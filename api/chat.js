const OPENAI_RESPONSES_URL = 'https://api.openai.com/v1/responses';
const OPENAI_MODELS_URL = 'https://api.openai.com/v1/models';

function sendJson(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(payload));
}

function getApiKey(req) {
  const value = req.headers['x-openai-api-key'];
  return Array.isArray(value) ? value[0] : String(value || '').trim();
}

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string' && req.body.trim()) return JSON.parse(req.body);
  let raw = '';
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 200000) throw new Error('Request quá lớn.');
  }
  return raw.trim() ? JSON.parse(raw) : {};
}

function isTextModel(id) {
  if (!id || typeof id !== 'string') return false;
  if (!/^(gpt-|o\d)/i.test(id)) return false;
  return !/(audio|realtime|transcribe|tts|image|search-preview|deep-research|moderation|embedding|whisper|dall-e|sora)/i.test(id);
}

function rankModel(id) {
  const preferred = [
    'gpt-5.2',
    'gpt-5.1',
    'gpt-5',
    'gpt-5-mini',
    'gpt-4.1',
    'gpt-4o',
    'gpt-4.1-mini',
    'gpt-4o-mini'
  ];
  const exact = preferred.indexOf(id);
  if (exact >= 0) return exact;
  if (/^gpt-5/i.test(id)) return 20;
  if (/^o[34]/i.test(id)) return 30;
  if (/^gpt-4\.1/i.test(id)) return 40;
  if (/^gpt-4o/i.test(id)) return 50;
  if (/^o\d/i.test(id)) return 60;
  return 100;
}

async function listAccessibleModels(apiKey) {
  const response = await fetch(OPENAI_MODELS_URL, {
    headers: { Authorization: `Bearer ${apiKey}` }
  });
  const raw = await response.text();
  let data = {};
  try { data = JSON.parse(raw); } catch {}
  if (!response.ok) return [];
  return (Array.isArray(data.data) ? data.data : [])
    .map(x => x && x.id)
    .filter(isTextModel)
    .sort((a, b) => rankModel(a) - rankModel(b) || a.localeCompare(b));
}

async function resolveModel(apiKey, requested) {
  const legacy = new Set(['gpt-5.6', 'gpt-5.6-terra', 'gpt-5.6-luna', 'chat-latest']);
  if (requested && !legacy.has(requested)) return requested;
  const models = await listAccessibleModels(apiKey);
  return models[0] || 'gpt-5-mini';
}

function cleanMessages(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter(x => x && (x.role === 'user' || x.role === 'assistant') && typeof x.content === 'string')
    .slice(-16)
    .map(x => ({ role: x.role, content: x.content.slice(0, 8000) }));
}

function buildInstructions(pageTitle, pageContext) {
  const title = String(pageTitle || 'CS115 · Toán cho Khoa học máy tính').slice(0, 300);
  const context = String(pageContext || '').slice(0, 16000);
  return [
    'Bạn là trợ giảng AI cho môn CS115 Toán cho Khoa học máy tính.',
    'Giải thích bằng tiếng Việt rõ ràng, theo từng bước, ưu tiên trực giác trước rồi mới đến công thức.',
    'Khi viết toán, dùng LaTeX chuẩn: công thức trong dòng dùng $...$; công thức riêng dòng dùng $$...$$.',
    'Không đặt công thức LaTeX trong code fence trừ khi người học hỏi về mã nguồn.',
    'Nếu câu hỏi liên quan bài học hiện tại, ưu tiên ngữ cảnh trang bên dưới. Nếu ngữ cảnh không đủ để khẳng định một chi tiết, nói rõ điều đó thay vì bịa.',
    `Trang hiện tại: ${title}`,
    context ? `Nội dung trang hiện tại:\n${context}` : 'Không có thêm nội dung trang.'
  ].join('\n\n');
}

function extractText(data) {
  if (typeof data?.output_text === 'string' && data.output_text.trim()) return data.output_text.trim();
  const parts = [];
  for (const item of Array.isArray(data?.output) ? data.output : []) {
    if (!item || item.type !== 'message') continue;
    for (const part of Array.isArray(item.content) ? item.content : []) {
      if (part?.type === 'output_text' && typeof part.text === 'string') parts.push(part.text);
      if (part?.type === 'refusal' && typeof part.refusal === 'string') parts.push(part.refusal);
    }
  }
  return parts.join('\n').trim();
}

async function callOpenAI(apiKey, model, messages, instructions) {
  const response = await fetch(OPENAI_RESPONSES_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model,
      instructions,
      input: messages
    })
  });
  const raw = await response.text();
  let data;
  try {
    data = JSON.parse(raw);
  } catch {
    return {
      ok: false,
      status: 502,
      data: { error: { message: 'OpenAI trả về phản hồi không phải JSON.', detail: raw.slice(0, 400) } }
    };
  }
  return { ok: response.ok, status: response.status, data };
}

function upstreamMessage(result) {
  return result?.data?.error?.message || result?.data?.message || `OpenAI HTTP ${result?.status || 500}`;
}

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') return sendJson(res, 200, { ok: true });
  if (req.method !== 'POST') return sendJson(res, 405, { error: 'Chỉ hỗ trợ POST.' });

  const apiKey = getApiKey(req);
  if (!apiKey) return sendJson(res, 400, { error: 'Thiếu OpenAI API key.' });

  let body;
  try {
    body = await readBody(req);
  } catch (error) {
    return sendJson(res, 400, { error: 'Request JSON không hợp lệ.', detail: error.message });
  }

  const messages = cleanMessages(body.messages);
  if (!messages.length || !messages.some(x => x.role === 'user')) {
    return sendJson(res, 400, { error: 'Không có câu hỏi hợp lệ.' });
  }

  try {
    let model = await resolveModel(apiKey, String(body.model || '').trim());
    const instructions = buildInstructions(body.pageTitle, body.pageContext);
    let result = await callOpenAI(apiKey, model, messages, instructions);

    if (!result.ok && (result.status === 400 || result.status === 404)) {
      const message = upstreamMessage(result);
      if (/model|not found|does not exist|unsupported/i.test(message)) {
        const models = await listAccessibleModels(apiKey);
        const fallback = models.find(x => x !== model);
        if (fallback) {
          model = fallback;
          result = await callOpenAI(apiKey, model, messages, instructions);
        }
      }
    }

    if (!result.ok) {
      return sendJson(res, result.status || 502, { error: upstreamMessage(result), model });
    }

    const reply = extractText(result.data);
    if (!reply) {
      return sendJson(res, 502, { error: 'OpenAI không trả về nội dung văn bản.', model });
    }

    return sendJson(res, 200, { reply, model });
  } catch (error) {
    return sendJson(res, 500, {
      error: 'Chatbot không thể kết nối tới OpenAI.',
      detail: error instanceof Error ? error.message : String(error)
    });
  }
};
