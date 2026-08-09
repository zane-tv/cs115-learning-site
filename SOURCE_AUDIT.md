# CS115 source audit

Rà soát ngày 2026-08-09 từ đúng 12 PDF học liệu đã cung cấp. Tổng cộng: **689 trang/slide**. Mục tiêu của đợt cập nhật này là đưa các bài học còn lại lên mức chi tiết tương đương **“Ma trận và phép tính ma trận – chuyên sâu”**: giải thích theo từng khái niệm, công thức LaTeX, ví dụ có bước giải, liên hệ ML, phòng lỗi thường gặp, lab tương tác và bài tập tự chấm.

## 1. Bản đồ nguồn -> bài học

| # | PDF nguồn | Số trang | Bài học chính | Nội dung nguồn được dùng |
|---|---|---:|---|---|
| 1 | `CS115.O11_Đề cương_Toan cho KHMT.pdf` | 8 | `de-cuong-mon-hoc` | Thông tin môn học, CG/CLO, yêu cầu, kế hoạch 15 tuần, đánh giá 40/60, tài liệu tham khảo |
| 2 | `CS115_Course_Introduction.pdf` | 20 | `gioi-thieu-mon-hoc` | 4 tín chỉ, phiên bản tổ chức 10 tuần, CLO, đánh giá, tổ chức buổi học, lộ trình tuần, công cụ và tài liệu |
| 3 | `CS115.01_Introduction to Machine Learning.pdf` | 39 | `tong-quan-may-hoc` | E–T–P, supervised/unsupervised/RL, classification/regression, features/labels, empirical risk, uncertainty, MLE, linear/polynomial regression, deep nets, overfitting, train/validation/test |
| 4 | `2024_02_CS115_Linear Algebra Review.pdf` | 17 | `dai-so-tuyen-tinh-review` | Linear systems, matrices, identity/inverse/transpose, matrix multiplication, solving systems, independence, basis/rank, vector-matrix form, dimension reduction |
| 5 | `Chương 1_Review ĐSTT (30_5).pdf` | 82 | `dai-so-tuyen-tinh-mo-rong` + nguồn cho `ma-tran-chuyen-sau` | Matrices, linear systems, vector space, linear combination, independence, spanning set, eigenpairs, inner product, norms, distances, angles, cosine, k-means, orthogonal/orthonormal sets, Gram–Schmidt, projection, positive-definite matrices |
| 6 | `2025_03_CS115_Analytic Geometry.pdf` | 126 | `hinh-hoc-giai-tich` | Inner product, norm, length/distance, KNN, validation/cross-validation, cosine similarity, clustering/k-means, orthogonal matrices/bases, Gram–Schmidt, orthogonal complement/projection, dimensionality reduction, eigenpairs, definiteness |
| 7 | `C1_Review Giai tich vector.pdf` | 20 | `giai-tich-vector-on-tap` | Derivative, partial derivative, gradient, chain rule, Jacobian, derivatives w.r.t. vectors/matrices, higher-order derivative, Hessian |
| 8 | `2024_04_CS115_Vector Caculus.pdf` | 131 | `giai-tich-vector-day-du` | Univariate differentiation, Taylor, multivariate partials/gradients, chain rule, Jacobian, matrix calculus, Hessian, optimization motivation, computational graphs, automatic differentiation, backpropagation, vectorized gradients, neural-network bridge |
| 9 | `C1_Review_XSTK.pdf` | 14 | `xac-suat-thong-ke` | Random variables, addition/multiplication rules, Bernoulli formula, total probability, Bayes, discrete/continuous density, expectation, variance, Binomial, Poisson, Normal |
| 10 | `LinearRegression_Tutorial.pdf` | 40 | `hoi-quy-tuyen-tinh` | Synthetic regression data, squared-error objective, gradient descent, from-scratch implementation, SGD vs GD vs normal equation, MAE/MSE/R², polynomial regression, Boston Housing practice |
| 11 | `OPTIMIZATION.pdf` | 108 | `toi-uu-hoa` | Optimization formulation, linear/least-squares/convex problems, single/multivariate optima, Hessian/positive definiteness, gradient/mini-batch/SGD, momentum, constrained optimization/Lagrange, convexity, quadratic forms, steepest descent, Newton, conjugate-gradient, Nelder–Mead |
| 12 | `CS115_Neuron_Network.pdf` | 84 | `mang-neural` | Linear classifier, softmax, neuron model, MLP architectures, activations, backprop, sequential vs batch, learning rate/stopping, generalization, early stopping/regularization, momentum, adaptive LR, second-order methods |

## 2. Các vùng nguồn chồng lấn

- **Đại số tuyến tính**: file 17 trang là bản review cô đọng; file 82 trang là nguồn mở rộng. Bài `dai-so-tuyen-tinh-review` giữ đúng phạm vi review; bài `dai-so-tuyen-tinh-mo-rong` dùng phần chi tiết hơn.
- **Ma trận**: `ma-tran-chuyen-sau` tiếp tục là deep-dive chuyên thao tác ma trận; không trộn toàn bộ vector-space/eigen/inner-product vào bài này.
- **Vector / Hình học giải tích**: file 82 trang và file 126 trang chồng lấn ở norm, distance, angle, orthogonality, projection, cosine và clustering. `hinh-hoc-giai-tich` ưu tiên cách tổ chức của file 126 trang; `vector-chuyen-sau` là bài thực hành riêng.
- **Giải tích vector**: file 20 trang là bản ôn nhanh; file 131 trang là bản đầy đủ có Taylor, computational graph, autodiff và backprop.
- **Hồi quy / ML intro**: file ML intro giới thiệu regression và overfitting; file Linear Regression Tutorial dùng làm nguồn thực hành chi tiết cho `hoi-quy-tuyen-tinh`.
- **Optimization / Neural Network**: cả hai nguồn có gradient methods. `toi-uu-hoa` trình bày thuật toán tối ưu như một chủ đề độc lập; `mang-neural` chỉ dùng các phương pháp tối ưu trong ngữ cảnh huấn luyện mạng.

## 3. Quy tắc cập nhật nội dung

1. **Nguồn chính là 12 PDF trên**. Không tự thêm một chương mới chỉ vì kiến thức đó phổ biến ngoài môn học.
2. Ví dụ tự học được phép biến đổi số hoặc rút gọn từ định nghĩa/công thức trong nguồn, và được gắn nhãn “Ví dụ tự học”.
3. Mỗi section hiển thị phạm vi slide/trang nguồn để người học biết nội dung xuất phát từ đâu.
4. Công thức được lưu dưới dạng LaTeX và typeset bằng KaTeX.
5. Mỗi bài kỹ thuật có lab tương tác phù hợp chủ đề và bài tập tự chấm; bài course/syllabus dùng timeline/checklist thay vì calculator toán học.
6. Những PDF/slide có metadata tiêu đề không khớp nội dung (ví dụ metadata cũ “Machine Learning: Overview”) được nhận diện theo **nội dung trang**, không theo metadata.
7. Các liên kết ngoài xuất hiện trong slide (website, blog, textbook) chỉ được ghi nhận là tài liệu tham khảo của slide; nội dung cập nhật không dựa vào việc tự động lấy thêm dữ liệu từ các liên kết đó.

## 4. Mức bao phủ sau cập nhật

- 14 bài học trong thư viện.
- 12 bài nền được dựng lại theo source audit này.
- 2 deep-dive (`ma-tran-chuyen-sau`, `vector-chuyen-sau`) được giữ như bài thực hành chuyên sâu.
- Mục tiêu bài tập toàn thư viện sau rebuild: **366 bài tự chấm** (gồm 60 bài của hai deep-dive hiện có).

## 5. Ghi chú kỹ thuật

Các PDF gốc hiện không được lưu trong repository GitHub mới, vì vậy UI mới hiển thị **tên file nguồn + phạm vi trang** thay cho link PDF bị 404. Khi các binary PDF được đưa lại vào `/sources`, có thể bật link tải nguồn mà không cần thay đổi nội dung bài học.
