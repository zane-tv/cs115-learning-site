from pathlib import Path
import json, re

PATH = Path('lesson-data/dai-so-tuyen-tinh-mo-rong.json')

def repair_json_backslashes(raw: str) -> str:
    out=[]; inside=False; i=0
    while i < len(raw):
        c=raw[i]
        if not inside:
            out.append(c)
            if c=='"': inside=True
            i+=1; continue
        if c=='"':
            out.append(c); inside=False; i+=1; continue
        if c!='\\':
            out.append(c); i+=1; continue
        n=raw[i+1] if i+1 < len(raw) else ''
        n2=raw[i+2] if i+2 < len(raw) else ''
        if n in '\\"/':
            out.extend([c,n]); i+=2; continue
        if n=='u' and re.fullmatch(r'[0-9a-fA-F]{4}', raw[i+2:i+6] or ''):
            out.append(raw[i:i+6]); i+=6; continue
        if n in 'bfnrt' and not n2.isalpha():
            out.extend([c,n]); i+=2; continue
        out.append('\\\\'); i+=1
    return ''.join(out)

raw=PATH.read_text(encoding='utf-8')
try:
    data=json.loads(raw)
except json.JSONDecodeError:
    data=json.loads(repair_json_backslashes(raw))

F=lambda latex,note=None,light=False: {'type':'formula','latex':latex,**({'note':note} if note else {}),**({'light':True} if light else {})}
P=lambda html: {'type':'p','html':html}
N=lambda title,html,style='note': {'type':'note','style':style,'title':title,'html':html}
B=lambda items: {'type':'bullets','items':items}
C=lambda items,cols=2: {'type':'cards','cols':cols,'items':items}
E=lambda title,steps,intro=None,result=None: {'type':'example','title':title,'steps':steps,**({'intro':intro} if intro else {}),**({'result':result} if result else {})}
T=lambda headers,rows: {'type':'table','headers':headers,'rows':rows}

data['subtitle']='Bản học chi tiết bám theo 82 slide ôn tập Đại số tuyến tính của CS115: đi từ ma trận và hệ tuyến tính đến không gian vector, tổ hợp tuyến tính, độc lập–hệ sinh, trị riêng, tích trong, norm–distance–cosine, trực giao–chiếu trực giao và ma trận xác định dương. Phần trực giao hóa Gram–Schmidt được ghi rõ là bổ sung từ tài liệu Hình học giải tích của cùng học phần.'
data['tags']=['Vector Space','Linear Combination','Basis','Eigenvalue','Inner Product','Norm','Cosine','Orthogonal','Projection','Positive Definite']
data['objectives']=[
    'Đọc đúng ký hiệu, kích thước vector/ma trận và hiểu Ax là tổ hợp tuyến tính các cột của A.',
    'Phân loại nghiệm của Ax=b bằng khử Gauss, pivot, biến tự do và rank.',
    'Giải thích được vector space, subspace, linear combination, span, linear independence và basis bằng cả đại số lẫn trực giác hình học.',
    'Tìm và kiểm tra eigenvalue/eigenvector từ Av=λv và det(A−λI)=0; hiểu vì sao eigenvector là hướng đặc biệt của phép biến đổi.',
    'Dùng inner product để xây dựng norm, distance, angle, cosine similarity, orthogonality và projection.',
    'Phân biệt orthogonal và orthonormal; hiểu vì sao một họ trực giao không chứa vector 0 là độc lập tuyến tính.',
    'Nhận biết positive definite / semidefinite / indefinite bằng quadratic form, dấu eigenvalue và các định thức con chính theo nội dung nguồn.',
    'Nhận ra các thuật ngữ Anh–Việt thường gặp trong slide, bài tập và code ML.'
]
data['sources']=[
    {'file':'Chương 1_Review ĐSTT (30_5).pdf','pages':'82 slide','note':'Nguồn chính; các section đều ghi khoảng slide tương ứng.'},
    {'file':'2025_03_CS115_Analytic Geometry.pdf','pages':'slide 92–96','note':'Nguồn bổ sung duy nhất cho thuật toán Gram–Schmidt tường minh; được đánh dấu riêng trong bài.'}
]
data['coverage']='Nội dung chính bám theo 82 slide Review ĐSTT: ma trận/hệ tuyến tính, vector space và ứng dụng, eigenpairs, inner product, norm, distance, cosine similarity, orthogonal/orthonormal, orthogonal projection và positive-definite matrices. Thuật toán Gram–Schmidt tường minh được tách thành phần bổ sung và dẫn sang slide 92–96 của Analytic Geometry, không gán nhầm cho nguồn 82 slide.'

data['sections']=[
{
'id':'notation-matrix','title':'Ký hiệu, vector và ma trận: đọc đúng trước khi tính','lead':'Đại số tuyến tính dễ sai ngay từ đầu nếu không theo dõi đối tượng là scalar, vector hay matrix và kích thước của chúng.','source':'Slide 4–14',
'blocks':[
P('Nguồn quy ước <b>x, y, z</b> cho vector; <b>A, B, X</b> cho ma trận; ký hiệu <b>ℝ</b> cho số thực, <b>ℝⁿ</b> cho không gian n chiều và <b>‖v‖</b> cho norm. Đây không chỉ là cách viết: kích thước quyết định phép toán nào hợp lệ.'),
F(r'\mathbf x\in\mathbb R^n,\qquad A\in\mathbb R^{m\times n}'),
C([
 {'title':'Vector','html':'Một dãy có thứ tự các thành phần. Có thể viết dạng cột để thuận tiện cho phép nhân ma trận.'},
 {'title':'Matrix','html':'Bảng m hàng × n cột. Có thể xem mỗi cột là một vector trong ℝᵐ.'},
 {'title':'Scalar','html':'Một số thực. Khi nhân scalar với vector/ma trận, mọi thành phần đều được nhân cùng scalar.'}
],3),
P('Điểm nối quan trọng với toàn bộ chương là <b>A x</b>. Nếu A có các cột a₁,…,aₙ và x=(x₁,…,xₙ)ᵀ thì A x chính là tổ hợp tuyến tính x₁a₁+⋯+xₙaₙ. Vì vậy hệ phương trình, span, độc lập tuyến tính và rank thực ra cùng nói về các cột của A.'),
F(r'A\mathbf x=x_1\mathbf a_1+x_2\mathbf a_2+\cdots+x_n\mathbf a_n', 'Cách nhìn theo cột của phép nhân ma trận.'),
C([
 {'title':'Transpose Aᵀ','html':'Đổi hàng thành cột: phần tử ở vị trí (i,j) chuyển sang (j,i).'},
 {'title':'Diagonal matrix','html':'Ma trận vuông có các phần tử ngoài đường chéo chính bằng 0.'},
 {'title':'Symmetric matrix','html':'A=Aᵀ. Tính đối xứng trở lại ở cuối bài khi xét positive definiteness.'},
 {'title':'Identity I','html':'Ma trận đơn vị; IA=AI=A khi kích thước phù hợp.'},
 {'title':'Zero matrix','html':'Mọi phần tử bằng 0; đóng vai trò phần tử 0 trong không gian ma trận.'},
 {'title':'Matrix product','html':'(AB)ᵢⱼ là tích vô hướng giữa hàng i của A và cột j của B.'}
],3),
N('Lỗi hay gặp','AB chỉ xác định khi số cột của A bằng số hàng của B. Nói “hai ma trận cùng kích thước thì nhân được” là sai; điều kiện cùng kích thước là điều kiện của phép cộng.', 'warning')
]},
{
'id':'linear-systems','title':'Hệ phương trình tuyến tính: từ hình học đến Ax=b','lead':'Một hệ tuyến tính vừa là bài toán tìm giao của các đối tượng hình học, vừa là bài toán tìm vector hệ số x để tạo ra b từ các cột của A.','source':'Slide 15–25',
'blocks':[
F(r'A\mathbf x=\mathbf b'),
P('Mỗi hàng của A tương ứng một phương trình, x chứa các ẩn và b là vế phải. Nếu b=0, nguồn gọi đây là <b>hệ tuyến tính thuần nhất</b> (homogeneous system). Hệ thuần nhất luôn có ít nhất nghiệm x=0.'),
C([
 {'title':'No solution','html':'Các ràng buộc mâu thuẫn; hình học 2D có thể là hai đường song song khác nhau.'},
 {'title':'Unique solution','html':'Các ràng buộc đủ độc lập để xác định đúng một điểm nghiệm.'},
 {'title':'Infinitely many','html':'Có biến tự do; nghiệm tạo thành một họ tham số.'}
],3),
P('Khử Gauss dùng các phép biến đổi sơ cấp trên hàng để tạo ma trận bậc thang. Mục tiêu không phải “thay đổi bài toán”, mà là viết một hệ tương đương dễ đọc pivot và biến tự do hơn.'),
B(['Đổi chỗ hai hàng.','Nhân một hàng với scalar khác 0.','Cộng vào một hàng một bội của hàng khác.']),
F(r'\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])', 'Điều kiện hệ tương thích.'),
T(['Trạng thái','Điều kiện rank','Ý nghĩa'],[
 ['Nghiệm duy nhất','rank(A)=rank([A|b])=n','Không có biến tự do.'],
 ['Vô số nghiệm','rank(A)=rank([A|b])<n','Có ít nhất một biến tự do.'],
 ['Vô nghiệm','rank(A)≠rank([A|b])','Ma trận bổ sung xuất hiện ràng buộc mâu thuẫn.']
]),
E('Ví dụ đọc nghiệm bằng rank',['Hàng thứ hai là 2 lần hàng thứ nhất nên chỉ có một phương trình độc lập.','rank(A)=rank([A|b])=1.','Có 2 ẩn nhưng chỉ 1 pivot, do đó có 1 biến tự do.'],'x+y=2, 2x+2y=4.','Hệ có vô số nghiệm, ví dụ x=t, y=2−t.'),
N('Nối sang vector space','Ax=b có nghiệm khi b nằm trong span của các cột A. Đây là cây cầu trực tiếp từ hệ tuyến tính sang hệ sinh.', 'deep')
]},
{
'id':'vector-space','title':'Không gian vector và không gian con','lead':'“Vector space” là khung chứa các đối tượng mà phép cộng vector và nhân scalar hoạt động nhất quán.','source':'Slide 26–29',
'blocks':[
P('Nguồn chuyển từ các vector cụ thể sang <b>không gian vector</b> (vector space) và nêu ứng dụng trong điều khiển–robot, xử lý ảnh/âm thanh, máy học, mật mã và kinh tế. Ý quan trọng để học là: vector không bắt buộc chỉ là mũi tên 2D/3D; nó là phần tử của một không gian có hai phép toán tuyến tính.'),
C([
 {'title':'Closure under addition','html':'Nếu u,v thuộc V thì u+v vẫn thuộc V.'},
 {'title':'Closure under scalar multiplication','html':'Nếu v thuộc V và α là scalar thì αv vẫn thuộc V.'},
 {'title':'Zero & inverse','html':'Có vector 0; mỗi v có vector đối −v để v+(−v)=0.'}
],3),
P('<b>Subspace</b> (không gian con) là một tập con vẫn giữ được cấu trúc vector space dưới chính hai phép toán đó. Khi kiểm tra một tập có là subspace hay không, tư duy thực dụng là kiểm tra nó chứa 0 và đóng dưới tổ hợp tuyến tính.'),
F(r'\alpha\mathbf u+\beta\mathbf v\in W\quad\text{với mọi }\mathbf u,\mathbf v\in W,\ \alpha,\beta\in\mathbb R'),
E('Ví dụ trực giác về subspace',['Mọi vector (x,y,0) nằm trên mặt phẳng z=0.','Cộng hai vector có tọa độ z bằng 0 vẫn cho z=0.','Nhân scalar cũng không làm xuất hiện thành phần z.','Vector 0=(0,0,0) thuộc tập.'],'W={(x,y,z)∈ℝ³ | z=0}.','W là một không gian con của ℝ³.'),
N('Điểm phân biệt','Một tập chỉ “trông giống đường/mặt phẳng” chưa đủ. Ví dụ một đường thẳng không đi qua gốc tọa độ không chứa vector 0, vì thế không là subspace của ℝ².', 'warning')
]},
{
'id':'linear-combination','title':'Tổ hợp tuyến tính: ngôn ngữ cốt lõi của cả chương','lead':'Tổ hợp tuyến tính trả lời câu hỏi: từ các vector đang có, ta tạo được những vector nào bằng cách co giãn rồi cộng?','source':'Slide 30–31',
'blocks':[
F(r'\mathbf w=c_1\mathbf v_1+c_2\mathbf v_2+\cdots+c_k\mathbf v_k'),
P('Các số c₁,…,cₖ là <b>coefficients</b> (hệ số). Mỗi hệ số cho phép đổi độ dài và có thể đảo hướng vector; phép cộng ghép các đóng góp đó thành vector mới. Khái niệm này xuất hiện lại trong Ax, span, basis và eigenvector.'),
E('Ví dụ tự học',['2v₁=(2,4).','−v₂=(−3,−1).','Cộng theo từng tọa độ: (2,4)+(−3,−1)=(−1,3).'],'v₁=(1,2), v₂=(3,1), w=2v₁−v₂.','w=(−1,3).'),
P('Nếu đặt các vector vᵢ làm cột của ma trận V và c=(c₁,…,cₖ)ᵀ thì toàn bộ tổ hợp tuyến tính viết gọn thành Vc. Do đó câu hỏi “w có là tổ hợp tuyến tính của v₁,…,vₖ không?” chính là câu hỏi hệ Vc=w có nghiệm không.'),
F(r'V\mathbf c=\mathbf w'),
N('Cách nghĩ khi giải bài','Đừng đoán hệ số bằng mắt khi số chiều lớn. Hãy dựng ma trận có các vector làm cột rồi giải hệ tuyến tính.', 'note')
]},
{
'id':'independence','title':'Độc lập tuyến tính và phụ thuộc tuyến tính','lead':'Độc lập tuyến tính đo xem trong một tập vector có hướng nào dư thừa hay không.','source':'Slide 32–38',
'blocks':[
F(r'c_1\mathbf v_1+\cdots+c_k\mathbf v_k=\mathbf0'),
P('Tập {v₁,…,vₖ} <b>độc lập tuyến tính</b> nếu phương trình trên chỉ có nghiệm tầm thường c₁=⋯=cₖ=0. Nếu tồn tại một bộ hệ số không đồng thời bằng 0 mà vẫn cho tổng bằng 0 thì tập <b>phụ thuộc tuyến tính</b>.'),
C([
 {'title':'Independent','html':'Không vector nào có thể tái tạo từ các vector còn lại. Mỗi hướng đóng góp thông tin mới.'},
 {'title':'Dependent','html':'Có ít nhất một quan hệ tuyến tính không tầm thường; một hoặc nhiều vector là dư thừa theo nghĩa tuyến tính.'}
],2),
P('Trong 2D, hai vector khác 0 cùng nằm trên một đường thẳng thì phụ thuộc; nếu không cùng phương thì độc lập. Hình học này rất hữu ích nhưng định nghĩa bằng hệ thuần nhất mới áp dụng cho mọi số chiều.'),
E('Kiểm tra bằng định thức trong 2D',['Dựng A=[v₁ v₂]=[[1,3],[2,1]].','det(A)=1·1−3·2=−5.','Định thức khác 0 nên A khả nghịch; Ac=0 chỉ có nghiệm c=0.'],'v₁=(1,2), v₂=(3,1).','Hai vector độc lập tuyến tính.'),
N('Không đồng nhất “độc lập” với “trực giao”','Trực giao khác 0 ⇒ độc lập. Nhưng độc lập không bắt buộc trực giao. Trực giao là điều kiện mạnh hơn và cần inner product.', 'warning')
]},
{
'id':'span-basis','title':'Hệ sinh, span và basis','lead':'Span mô tả toàn bộ những gì một tập vector có thể tạo ra; basis là một hệ sinh không dư thừa.','source':'Slide 39–40',
'blocks':[
F(r'\operatorname{span}\{\mathbf v_1,\ldots,\mathbf v_k\}=\left\{\sum_{i=1}^{k}c_i\mathbf v_i:c_i\in\mathbb R\right\}'),
P('<b>Spanning set</b> (hệ sinh/tập sinh) là tập vector có span bằng không gian đang xét. Một hệ sinh có thể chứa vector dư thừa. <b>Basis</b> (cơ sở) vừa sinh được toàn bộ không gian, vừa độc lập tuyến tính.'),
C([
 {'title':'Span','html':'Tập tất cả tổ hợp tuyến tính có thể tạo được.'},
 {'title':'Spanning set','html':'Tập vector đủ để sinh toàn bộ không gian mục tiêu.'},
 {'title':'Basis','html':'Spanning set + linear independence.'}
],3),
P('Ý nghĩa quan trọng của basis là <b>biểu diễn duy nhất</b>: khi basis cố định, mỗi vector trong không gian có đúng một bộ tọa độ theo basis đó. Đây là lý do thay basis có thể đổi cách biểu diễn dữ liệu mà không đổi chính vector trừu tượng.'),
E('Cơ sở chuẩn ℝ²',['e₁=(1,0), e₂=(0,1) độc lập.','Mọi (x,y)=x e₁+y e₂ nên chúng sinh ℝ².','Vì vừa độc lập vừa sinh toàn bộ ℝ², {e₁,e₂} là basis.'],'','Tọa độ của vector (3,−2) theo basis chuẩn là (3,−2).'),
N('Rank nhìn theo basis','Rank(A) có thể hiểu là số hướng độc lập trong các cột (đồng thời bằng dimension của column space). Vì thế rank là một phép đo “bao nhiêu thông tin tuyến tính độc lập” mà A chứa.', 'deep')
]},
{
'id':'eigen','title':'Trị riêng và vector riêng: hướng không bị xoay khỏi chính nó','lead':'Eigenvector là vector khác 0 mà sau phép biến đổi A vẫn nằm trên cùng đường thẳng với chính nó; eigenvalue cho hệ số co giãn/đảo hướng.','source':'Slide 41–47',
'blocks':[
F(r'A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\neq\mathbf0'),
P('Công thức nói rằng tác động của A lên v không tạo một hướng mới: kết quả chỉ là λ lần v. Nếu λ>1 thì độ lớn theo hướng đó tăng; 0<λ<1 thì co lại; λ<0 thì đồng thời đảo hướng; λ=0 thì hướng đó bị đưa về vector 0.'),
E('Ví dụ đúng theo mạch nguồn',['A v = [[1,2],[1,0]]·(2,1)ᵀ = (4,2)ᵀ.','(4,2)ᵀ = 2(2,1)ᵀ.','Vì v≠0 và Av=2v, v là eigenvector.'],'A=[[1,2],[1,0]], v=(2,1)ᵀ.','λ=2.'),
P('Để tìm λ khi chưa biết v, chuyển Av=λv thành (A−λI)v=0. Muốn tồn tại nghiệm v≠0, ma trận A−λI phải suy biến; do đó determinant của nó bằng 0.'),
F(r'(A-\lambda I)\mathbf v=\mathbf0,\qquad \det(A-\lambda I)=0'),
E('Ví dụ λ=7 từ nguồn',['A−7I=[[-6,6],[5,−5]].','Giải (A−7I)x=0 cho x₁=x₂.','Nghiệm khác 0 có dạng x=t(1,1)ᵀ, t≠0.'],'A=[[1,6],[5,2]].','7 là eigenvalue; mọi bội khác 0 của (1,1)ᵀ là eigenvector tương ứng.'),
B(['Nếu v là eigenvector ứng với λ thì kv với k≠0 cũng là eigenvector cùng λ.','Các tổ hợp tuyến tính không tầm thường của các eigenvector độc lập cùng λ vẫn nằm trong cùng không gian nghiệm của (A−λI)v=0.','Ma trận vuông bậc n có n eigenvalue khi tính cả bội trong miền phức.','Với ma trận đối xứng thực, các eigenvalue đều thực.','Nguồn nối trực tiếp positive definite với việc mọi eigenvalue đều dương.']),
N('Lỗi định nghĩa','Vector 0 không bao giờ được gọi là eigenvector, dù A0=λ0 đúng với mọi λ.', 'warning')
]},
{
'id':'inner-product','title':'Tích trong: từ đại số sang hình học','lead':'Inner product tạo ra một số từ hai vector, đồng thời là nền để định nghĩa độ dài, góc và trực giao.','source':'Slide 48–54',
'blocks':[
F(r'\langle\cdot,\cdot\rangle:V\times V\to\mathbb R'),
B(['Đối xứng trong không gian thực: ⟨u,v⟩=⟨v,u⟩.','Phân phối theo phép cộng: ⟨u+v,w⟩=⟨u,w⟩+⟨v,w⟩.','Tương thích nhân scalar: ⟨cu,v⟩=c⟨u,v⟩.','Xác định dương: ⟨v,v⟩≥0 và bằng 0 khi và chỉ khi v=0.']),
P('Trong ℝⁿ với Euclidean inner product, inner product chính là <b>dot product</b>.'),
F(r'\langle\mathbf u,\mathbf v\rangle=\mathbf u^T\mathbf v=\sum_{i=1}^{n}u_i v_i'),
E('Ví dụ trực giao',['u·v=2(−1)+(−1)4+3·2.','=−2−4+6=0.','Hai vector đều khác 0.'],'u=(2,−1,3), v=(−1,4,2).','u và v trực giao theo Euclidean inner product.'),
N('Không phải mọi công thức “nhân tọa độ rồi cộng” đều là inner product','Một ánh xạ muốn là inner product phải thỏa đủ các tính chất, đặc biệt positive definiteness. Nguồn có ví dụ phản chứng bằng cách chọn vector làm ⟨v,v⟩ không dương.', 'warning')
]},
{
'id':'norm','title':'Norm: độ lớn tổng quát của vector','lead':'Norm ánh xạ vector thành một số không âm và phải hành xử giống một khái niệm độ dài.','source':'Slide 55–57',
'blocks':[
B(['Không âm và xác định: ‖v‖≥0; ‖v‖=0 ⇔ v=0.','Đồng bậc: ‖αv‖=|α|‖v‖.','Bất đẳng thức tam giác: ‖u+v‖≤‖u‖+‖v‖.']),
F(r'\|\mathbf v\|_p=\left(\sum_{i=1}^{n}|v_i|^p\right)^{1/p}'),
T(['Norm','Công thức','Cách đọc'],[
 ['ℓ₁ / Manhattan','Σ|vᵢ|','Tổng độ lớn từng tọa độ.'],
 ['ℓ₂ / Euclidean','√(Σvᵢ²)','Độ dài Euclid; bằng √(vᵀv).'],
 ['ℓ∞','max |vᵢ|','Chỉ nhìn thành phần có độ lớn lớn nhất.']
]),
F(r'\|\mathbf v\|_1=\sum_i|v_i|,\qquad \|\mathbf v\|_2=\sqrt{\mathbf v^T\mathbf v},\qquad \|\mathbf v\|_\infty=\max_i|v_i|'),
E('Cùng một vector, nhiều norm',['‖(3,−4)‖₁=|3|+|−4|=7.','‖(3,−4)‖₂=√(9+16)=5.','‖(3,−4)‖∞=max(3,4)=4.'],'v=(3,−4).','Norm không phải một công thức duy nhất; phải biết đang dùng norm nào.'),
N('Normalization','Nếu dùng L2 normalization, ta chia vector khác 0 cho ‖v‖₂ để thu vector đơn vị cùng hướng. Đây là thao tác khác với “standardization” trong thống kê.', 'note')
]},
{
'id':'distance','title':'Khoảng cách: đo độ khác nhau bằng norm của hiệu','lead':'Distance biến hai điểm/vector thành một số không âm; với Euclidean geometry, nó là norm L2 của vector hiệu.','source':'Slide 58–65',
'blocks':[
F(r'd(\mathbf u,\mathbf v)=\|\mathbf u-\mathbf v\|'),
P('Cách đọc hình học: u−v là vector dịch chuyển từ v đến u; norm của vector dịch chuyển đó là độ dài đoạn nối hai điểm. Vì vậy distance được xây từ norm một cách tự nhiên.'),
E('Euclidean distance',['u−v=(3−0,4−0)=(3,4).','‖u−v‖₂=√(3²+4²)=5.'],'u=(3,4), v=(0,0).','d₂(u,v)=5.'),
P('Nguồn minh họa khoảng cách giữa các văn bản Wikipedia sau khi mỗi tài liệu được biểu diễn bằng vector đặc trưng tần suất từ trên một từ điển 4423 từ. Đây là ví dụ quan trọng: distance không chỉ dành cho điểm 2D; nó hoạt động trên vector chiều rất cao.'),
N('Khoảng cách phụ thuộc biểu diễn','Nếu ta đổi feature scale hoặc đổi norm, các cặp điểm được xem là “gần/xa” có thể thay đổi. Nguồn dùng ví dụ văn bản để cho thấy hình học vector được áp lên dữ liệu.', 'deep')
]},
{
'id':'cosine','title':'Góc và cosine similarity: so sánh hướng thay vì chỉ độ dài','lead':'Cosine similarity chuẩn hóa inner product bởi độ dài hai vector, tạo thước đo phụ thuộc chủ yếu vào hướng.','source':'Slide 66–69',
'blocks':[
F(r'\cos\theta=\frac{\langle\mathbf u,\mathbf v\rangle}{\|\mathbf u\|\,\|\mathbf v\|}', 'Hai vector phải khác 0.'),
C([
 {'title':'cos θ ≈ 1','html':'Hai vector gần cùng hướng.'},
 {'title':'cos θ = 0','html':'Hai vector trực giao; góc 90° trong Euclidean geometry.'},
 {'title':'cos θ ≈ −1','html':'Hai vector gần ngược hướng.'}
],3),
P('Điểm khác với Euclidean distance: nếu nhân một vector với scalar dương, hướng không đổi nên cosine similarity không đổi, trong khi khoảng cách Euclid thường thay đổi. Vì vậy cosine thường phù hợp khi độ lớn tuyệt đối ít quan trọng hơn “mẫu phân bố theo tọa độ”.'),
E('Ví dụ',['u·v=1·2+2·4=10.','‖u‖=√5, ‖v‖=√20=2√5.','cosθ=10/(√5·2√5)=1.'],'u=(1,2), v=(2,4).','Hai vector cùng hướng dù độ dài khác nhau.'),
N('Trường hợp vector 0','Cosine similarity không xác định nếu một vector có norm bằng 0 vì mẫu số bằng 0.', 'warning')
]},
{
'id':'orthogonal','title':'Trực giao và trực chuẩn','lead':'Orthogonal nói về góc vuông qua inner product; orthonormal thêm điều kiện mỗi vector có norm bằng 1.','source':'Slide 70–71',
'blocks':[
F(r'\langle\mathbf u_i,\mathbf u_j\rangle=0\quad(i\neq j)'),
P('Hai vector u₁,u₂ trực giao khi và chỉ khi inner product của chúng bằng 0. Một họ S={u₁,…,uₚ} trực giao nếu mọi cặp khác chỉ số đều trực giao.'),
F(r'\langle\mathbf u_i,\mathbf u_j\rangle=\delta_{ij}', 'Cách viết gọn cho một họ orthonormal: 0 khi i≠j, 1 khi i=j.'),
P('Một họ <b>orthonormal</b> vừa trực giao vừa có ‖uᵢ‖=1. Nếu một basis đồng thời orthogonal/orthonormal thì gọi là orthogonal/orthonormal basis.'),
B(['Một họ trực giao không chứa vector 0 là độc lập tuyến tính.','Trong không gian tích trong n chiều, một họ trực giao gồm n vector khác 0 là một orthogonal basis.','Nguồn nêu rằng từ một họ độc lập tuyến tính có thể thay bằng một họ trực giao/trực chuẩn giữ nguyên các span lũy tiến.']),
P('Vì sao trực giao ⇒ độc lập? Nếu c₁u₁+⋯+cₖuₖ=0, lấy inner product hai vế với uⱼ. Mọi hạng i≠j biến mất do trực giao, còn cⱼ‖uⱼ‖²=0. Vì uⱼ≠0 nên ‖uⱼ‖²>0, suy ra cⱼ=0. Lặp cho mọi j.'),
N('Trực chuẩn giúp tính toán đơn giản','Khi basis trực chuẩn, hệ số tọa độ theo một hướng qᵢ có thể lấy trực tiếp bằng inner product ⟨x,qᵢ⟩ thay vì giải một hệ tuyến tính tổng quát.', 'deep')
]},
{
'id':'projection','title':'Phép chiếu trực giao: lấy phần của u theo hướng v','lead':'Projection tách một vector thành thành phần song song với v và phần còn lại vuông góc với v.','source':'Slide 72–74',
'blocks':[
F(r'\operatorname{proj}_{\mathbf v}(\mathbf u)=\frac{\langle\mathbf u,\mathbf v\rangle}{\langle\mathbf v,\mathbf v\rangle}\mathbf v,\qquad \mathbf v\neq\mathbf0'),
P('Hệ số ⟨u,v⟩/⟨v,v⟩ chọn đúng độ dài có dấu trên hướng v. Kết quả projection luôn là một bội của v, nên nằm trên span{v}.'),
P('Đặt p=projᵥ(u) và r=u−p. Ý nghĩa “orthogonal projection” là r trực giao với v: ⟨r,v⟩=0. Đây là tiêu chuẩn kiểm tra kết quả rất mạnh.'),
F(r'\mathbf u=\operatorname{proj}_{\mathbf v}(\mathbf u)+\mathbf r,\qquad \langle\mathbf r,\mathbf v\rangle=0'),
E('Ví dụ theo nguồn',['⟨u,v⟩=6·1+2·2+4·0=10.','⟨v,v⟩=1²+2²+0²=5.','Hệ số chiếu=10/5=2.','projᵥ(u)=2(1,2,0)=(2,4,0).'],'u=(6,2,4), v=(1,2,0).','Hình chiếu trực giao là (2,4,0).'),
N('Nếu v là unit vector','Khi ‖v‖=1 thì ⟨v,v⟩=1 và công thức rút gọn thành projᵥ(u)=⟨u,v⟩v.', 'note')
]},
{
'id':'gram-schmidt','title':'Bổ sung: trực giao hóa Gram–Schmidt','lead':'Phần này làm tường minh định lý trực giao hóa ở slide 71 bằng thuật toán Gram–Schmidt từ tài liệu Analytic Geometry của cùng học phần.','source':'Nguồn bổ sung: 2025_03_CS115_Analytic Geometry, slide 92–96',
'blocks':[
N('Phân biệt nguồn','Review ĐSTT 82 slide nêu định lý có thể thay một họ độc lập bằng họ trực giao/trực chuẩn giữ cùng span. Công thức thuật toán bên dưới lấy từ Analytic Geometry, không gán vào 82 slide Review.', 'note'),
P('Gram–Schmidt xử lý từng vector theo thứ tự. Ở bước i, ta trừ khỏi aᵢ tất cả các thành phần đã nằm trên các hướng trực chuẩn q₁,…,qᵢ₋₁. Phần còn lại q̃ᵢ vuông góc với các q trước; sau đó chuẩn hóa thành qᵢ.'),
F(r'\widetilde{\mathbf q}_i=\mathbf a_i-\sum_{j=1}^{i-1}(\mathbf q_j^T\mathbf a_i)\mathbf q_j'),
F(r'\mathbf q_i=\frac{\widetilde{\mathbf q}_i}{\|\widetilde{\mathbf q}_i\|}'),
B(['Nếu q̃ᵢ=0, vector aᵢ đã nằm trong span của các vector trước: tập đầu vào phụ thuộc tuyến tính.','Nếu thuật toán không dừng sớm, các vector đầu vào độc lập và ta thu được một họ orthonormal.','Thứ tự vector đầu vào có thể thay đổi các vector q cụ thể nhưng span cuối cùng vẫn là không gian do tập ban đầu sinh ra.']),
N('Trực giác','Mỗi bước là “bóc bỏ phần đã biết” khỏi vector mới, rồi chỉ giữ hướng thông tin mới và chuẩn hóa nó.', 'deep')
]},
{
'id':'applications','title':'Ứng dụng hình học vector: dữ liệu, distance và k-means','lead':'Nguồn dùng không gian vector để kết nối các khái niệm đại số với dữ liệu nhiều chiều.','source':'Khoảng slide 58–69 và phần Applications',
'blocks':[
P('Khi một đối tượng dữ liệu được mã hóa thành vector feature, các khái niệm vừa học trở thành công cụ so sánh: norm đo độ lớn, distance đo độ gần, cosine đo tương đồng hướng, inner product đo mức liên hệ tuyến tính theo hình học đã chọn.'),
F(r'\boldsymbol\mu_k=\frac{1}{|C_k|}\sum_{\mathbf x_i\in C_k}\mathbf x_i', 'Centroid của cluster Cₖ.'),
P('Trong k-means, centroid là trung bình vector của các điểm đang thuộc cluster. Quy trình lặp giữa gán điểm vào centroid gần và cập nhật centroid. Bài này chỉ dùng k-means như ví dụ ứng dụng của vector/distance đúng mức nguồn, không mở rộng thành một chương clustering.'),
B(['Biểu diễn đối tượng thành vector.','Chọn K centroid ban đầu.','Gán mỗi điểm vào centroid gần nhất theo distance được chọn.','Cập nhật mỗi centroid bằng trung bình các vector trong cluster.','Lặp cho đến khi việc gán/centroid ổn định theo tiêu chí triển khai.']),
N('Điều cần nhớ','K-means phụ thuộc mạnh vào cách biểu diễn feature và thước đo khoảng cách. Đây là lý do hiểu norm/distance trước khi dùng thuật toán ML là quan trọng.', 'deep')
]},
{
'id':'positive-definite','title':'Ma trận xác định dương: năng lượng luôn dương theo mọi hướng khác 0','lead':'Positive definiteness nối đại số ma trận với quadratic form và dấu eigenvalue.','source':'Slide 75–82',
'blocks':[
P('Nguồn xét ma trận vuông đối xứng thực A và biểu thức <b>xᵀAx</b>. Đây là một scalar phụ thuộc vào hướng x. Dấu của scalar này trên mọi x≠0 quyết định loại definiteness.'),
F(r'\mathbf x^T A\mathbf x>0\quad\forall\mathbf x\neq\mathbf0', 'A positive definite (PD).'),
T(['Loại','Điều kiện quadratic form','Dấu eigenvalue với A đối xứng'],[
 ['Positive definite','xᵀAx>0 với mọi x≠0','Tất cả >0'],
 ['Positive semidefinite','xᵀAx≥0','Tất cả ≥0'],
 ['Negative definite','xᵀAx<0','Tất cả <0'],
 ['Negative semidefinite','xᵀAx≤0','Tất cả ≤0'],
 ['Indefinite','Có hướng cho giá trị dương và hướng cho giá trị âm','Có cả eigenvalue dương và âm']
]),
P('Vì A đối xứng thực có eigenvalue thực, ta có thể kiểm tra definiteness bằng dấu của các eigenvalue. Nếu Av=λv với v≠0 thì trên chính eigenvector đó, vᵀAv=λ‖v‖²; vì ‖v‖²>0 nên dấu của quadratic form theo hướng v chính là dấu của λ.'),
F(r'\mathbf v^T A\mathbf v=\lambda\,\mathbf v^T\mathbf v=\lambda\|\mathbf v\|_2^2'),
P('Nguồn cũng dùng tiêu chuẩn định thức con chính (principal-minor / leading principal-minor test trong trường hợp đối xứng) để nhận biết positive definite. Ở ví dụ cuối, các định thức con chính đầu lần lượt dương nên kết luận ma trận xác định dương.'),
F(r'\det(A_1)>0,\ \det(A_2)>0,\ \ldots,\ \det(A_n)>0', 'Sylvester criterion cho ma trận đối xứng thực: các leading principal minors dương ⇔ positive definite.'),
E('Ví dụ rất đơn giản',['xᵀAx=2x₁²+x₂².','Nếu x≠0 thì ít nhất một trong x₁,x₂ khác 0.','Do đó 2x₁²+x₂²>0.'],'A=diag(2,1).','A positive definite.'),
N('PD khác PSD','PSD cho phép tồn tại x≠0 với xᵀAx=0; PD thì không. Trên eigenvalue, PSD cho phép λ=0 còn PD yêu cầu mọi λ>0.', 'warning')
]},
{
'id':'concept-map','title':'Bản đồ khái niệm: vì sao các phần này nối với nhau','lead':'Thay vì học từng định nghĩa rời rạc, hãy nhìn chương như một chuỗi câu hỏi về “hướng thông tin” trong không gian.','source':'Tổng hợp từ slide 6, 26–82',
'blocks':[
T(['Câu hỏi','Khái niệm trả lời','Công cụ'],[
 ['b có tạo từ các cột A không?','Span / linear system','Giải Ax=b'],
 ['Các hướng có dư thừa không?','Linear independence','Giải Ac=0 / rank'],
 ['Bộ hướng tối thiểu để biểu diễn?','Basis','Independent + spanning'],
 ['Hướng nào A chỉ co giãn?','Eigenvector','Av=λv'],
 ['Hai vector “vuông góc” không?','Inner product / orthogonal','⟨u,v⟩=0'],
 ['Vector dài bao nhiêu?','Norm','‖v‖'],
 ['Hai điểm cách nhau bao xa?','Distance','‖u−v‖'],
 ['Hai vector cùng hướng đến mức nào?','Cosine similarity','⟨u,v⟩/(‖u‖‖v‖)'],
 ['Phần nào của u nằm theo v?','Projection','projᵥ(u)'],
 ['Quadratic form có luôn dương?','Positive definiteness','xᵀAx / eigenvalues / minors']
]),
N('Mạch học nên nhớ','Ax=b → linear combination → span → independence → basis → eigen → inner product → norm/distance/angle → orthogonal/projection → positive definiteness. Nếu giữ được mạch này, các công thức ít bị rời rạc.', 'success')
]}
]

data['glossary']=[
['Scalar','Vô hướng; một số đơn lẻ dùng để co giãn vector/ma trận.'],
['Vector','Vectơ; phần tử của vector space, trong ℝⁿ thường biểu diễn bằng n tọa độ có thứ tự.'],
['Matrix','Ma trận; bảng số m×n, cũng có thể nhìn như một tập các vector cột.'],
['Dimension / size','Kích thước; vector có số thành phần, ma trận có số hàng × số cột.'],
['Transpose','Chuyển vị; đổi hàng thành cột, ký hiệu Aᵀ.'],
['Diagonal matrix','Ma trận đường chéo; ma trận vuông có phần tử ngoài đường chéo chính bằng 0.'],
['Symmetric matrix','Ma trận đối xứng; A=Aᵀ.'],
['Identity matrix','Ma trận đơn vị I; phần tử trung hòa của phép nhân ma trận.'],
['Zero matrix','Ma trận không; mọi phần tử bằng 0.'],
['Matrix multiplication','Phép nhân ma trận; mỗi phần tử kết quả là tích vô hướng một hàng với một cột.'],
['Linear system','Hệ phương trình tuyến tính; có thể viết gọn dưới dạng Ax=b.'],
['Homogeneous system','Hệ tuyến tính thuần nhất; Ax=0.'],
['Augmented matrix','Ma trận bổ sung [A|b] dùng khi khử Gauss.'],
['Elementary row operation','Phép biến đổi sơ cấp trên hàng; đổi hàng, nhân hàng với số khác 0, cộng bội của hàng khác.'],
['Gaussian elimination','Phương pháp khử Gauss; đưa hệ về dạng bậc thang để đọc nghiệm.'],
['Pivot','Vị trí trụ trong dạng bậc thang; gắn với biến cơ sở.'],
['Free variable','Biến tự do; biến không có pivot tương ứng và có thể dùng làm tham số nghiệm.'],
['Rank','Hạng; số hướng tuyến tính độc lập của hàng/cột, hay dimension của column space.'],
['Consistent system','Hệ tương thích; hệ có ít nhất một nghiệm.'],
['Vector space','Không gian vector; tập đối tượng đóng dưới cộng vector và nhân scalar, thỏa các tiên đề tuyến tính.'],
['Subspace','Không gian con; tập con vẫn là vector space với cùng phép cộng và nhân scalar.'],
['Closure','Tính đóng; thực hiện phép toán hợp lệ trên phần tử của tập vẫn thu phần tử trong tập.'],
['Linear combination','Tổ hợp tuyến tính c₁v₁+⋯+cₖvₖ.'],
['Coefficient','Hệ số cᵢ trong một tổ hợp tuyến tính.'],
['Linear independence','Độc lập tuyến tính; c₁v₁+⋯+cₖvₖ=0 chỉ có nghiệm tất cả cᵢ=0.'],
['Linear dependence','Phụ thuộc tuyến tính; tồn tại quan hệ tuyến tính không tầm thường cho tổng bằng 0.'],
['Span','Không gian sinh; tập tất cả tổ hợp tuyến tính của một tập vector.'],
['Spanning set','Hệ sinh/tập sinh; tập vector có span bằng không gian mục tiêu.'],
['Basis','Cơ sở; một spanning set đồng thời độc lập tuyến tính.'],
['Coordinate vector','Vector tọa độ; bộ hệ số biểu diễn một vector theo một basis đã chọn.'],
['Eigenvalue','Trị riêng λ; scalar trong quan hệ Av=λv với v≠0.'],
['Eigenvector','Vector riêng v; hướng khác 0 mà A chỉ co giãn/đảo hướng bằng λ.'],
['Characteristic equation','Phương trình đặc trưng det(A−λI)=0 để tìm eigenvalue.'],
['Inner product','Tích trong; ánh xạ hai vector thành scalar và thỏa đối xứng, tuyến tính, xác định dương trong không gian thực.'],
['Dot product','Tích vô hướng Euclid uᵀv=Σuᵢvᵢ; một inner product chuẩn trên ℝⁿ.'],
['Norm','Chuẩn; khái niệm độ dài tổng quát thỏa không âm, đồng bậc và bất đẳng thức tam giác.'],
['p-norm','Chuẩn ℓp: (Σ|vᵢ|ᵖ)^(1/p).'],
['Manhattan norm / ℓ1','Chuẩn L1; tổng trị tuyệt đối các tọa độ.'],
['Euclidean norm / ℓ2','Chuẩn L2; căn tổng bình phương, bằng √(vᵀv).'],
['Infinity norm / ℓ∞','Chuẩn vô cực; trị tuyệt đối lớn nhất trong các tọa độ.'],
['Unit vector','Vector đơn vị; vector có norm bằng 1.'],
['Normalization','Chuẩn hóa độ dài; thường là chia vector khác 0 cho norm để thu unit vector.'],
['Distance','Khoảng cách; thường d(u,v)=‖u−v‖ với norm đã chọn.'],
['Cosine similarity','Độ tương tự cosine; inner product chia cho tích hai norm, đo mức tương đồng về hướng.'],
['Orthogonal','Trực giao; hai vector có inner product bằng 0.'],
['Orthogonal set','Họ trực giao; mọi cặp vector khác nhau trong họ đều trực giao.'],
['Orthonormal','Trực chuẩn; trực giao và mọi vector có norm bằng 1.'],
['Orthogonal basis','Cơ sở trực giao; basis đồng thời là một họ trực giao.'],
['Orthonormal basis','Cơ sở trực chuẩn; basis mà các vector đôi một trực giao và đều có norm 1.'],
['Orthogonal projection','Phép chiếu trực giao; thành phần của u nằm trên span của v sao cho phần dư vuông góc với v.'],
['Gram–Schmidt','Thuật toán trực giao hóa một họ độc lập tuyến tính; trong bài này lấy công thức tường minh từ Analytic Geometry slide 92–96.'],
['Centroid','Tâm cụm; vector trung bình của các điểm trong một cluster.'],
['k-means','Thuật toán phân cụm lặp giữa gán điểm vào centroid gần nhất và cập nhật centroid.'],
['Quadratic form','Dạng toàn phương xᵀAx; scalar dùng để xét dấu của ma trận đối xứng.'],
['Positive definite (PD)','Xác định dương; xᵀAx>0 với mọi x≠0.'],
['Positive semidefinite (PSD)','Nửa xác định dương; xᵀAx≥0, cho phép có hướng khác 0 cho giá trị 0.'],
['Negative definite','Xác định âm; xᵀAx<0 với mọi x≠0.'],
['Indefinite','Không xác định dấu; quadratic form nhận cả giá trị dương lẫn âm theo các hướng khác nhau.'],
['Principal minor','Định thức con chính; determinant của ma trận con lấy cùng tập chỉ số hàng và cột.'],
['Leading principal minor','Định thức con chính đầu; lấy k hàng và k cột đầu, dùng trong tiêu chuẩn Sylvester cho ma trận đối xứng.'],
['Sylvester criterion','Tiêu chuẩn: ma trận đối xứng thực positive definite khi và chỉ khi mọi leading principal minor đều dương.']
]

PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('updated', PATH)
print('sections', len(data['sections']), 'glossary', len(data['glossary']), 'exercises', len(data.get('exercises',[])))
# Validate the written JSON strictly.
json.loads(PATH.read_text(encoding='utf-8'))
