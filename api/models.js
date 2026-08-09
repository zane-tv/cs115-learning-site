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

function isTextModel(id) {
  if (!id || typeof id !== 'string') return false;
  if (!/^(gpt-|o\d|chatgpt-)/i.test(id)) return false;
  return !/(audio|realtime|transcribe|tts|image|vision-preview|search-preview|deep-research|moderation|embedding|whisper|dall-e|sora)/i.test(id);
}

function modelRank(id) {
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

function labelFor(id) {
  if (/mini/i.test(id)) return id + ' · nhanh / tiết kiệm';
  if (/nano/i.test(id)) return id + ' · rất nhanh';
  if (/^gpt-5(?:\.|$)/i.test(id)) return id + ' · ưu tiên';
  return id;
}

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') return sendJson(res, 200, { ok: true });
  if (req.method !== 'POST') return sendJson(res, 405, { error: 'Chỉ hỗ trợ POST.' });

  const apiKey = getApiKey(req);
  if (!apiKey) return sendJson(res, 400, { error: 'Thiếu OpenAI API key.' });

  try {
    const upstream = await fetch(OPENAI_MODELS_URL, {
      headers: { Authorization: `Bearer ${apiKey}` }
    });
    const raw = await upstream.text();
    let data;
    try {
      data = JSON.parse(raw);
    } catch {
      return sendJson(res, 502, {
        error: 'OpenAI trả về phản hồi không phải JSON khi tải danh sách model.',
        detail: raw.slice(0, 300)
      });
    }

    if (!upstream.ok) {
      const message = data?.error?.message || data?.message || `OpenAI HTTP ${upstream.status}`;
      return sendJson(res, upstream.status, { error: message });
    }

    const models = (Array.isArray(data.data) ? data.data : [])
      .map(x => x && x.id)
      .filter(isTextModel)
      .sort((a, b) => modelRank(a) - modelRank(b) || a.localeCompare(b))
      .slice(0, 80)
      .map(id => ({ id, label: labelFor(id) }));

    const preferredModel = models[0]?.id || '';
    return sendJson(res, 200, { models, preferredModel });
  } catch (error) {
    return sendJson(res, 500, {
      error: 'Không thể kết nối tới OpenAI Models API.',
      detail: error instanceof Error ? error.message : String(error)
    });
  }
};
