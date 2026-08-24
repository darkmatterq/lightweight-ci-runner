# 📌 ĐẶC TẢ DỰ ÁN: LIGHTWEIGHT GITOPS CI/CD PIPELINE & BUILD ENGINE

## 🎯 1. Mục tiêu Dự án
- Xây dựng một hệ thống CI/CD Runner Engine tự phát triển (không copy mẫu trên mạng) nhằm tạo điểm sáng kỹ thuật vượt trội trong CV ứng tuyển vị trí DevOps Intern / Junior DevOps.
- Dự án kết hợp hoàn chỉnh cả 6 kỹ năng cốt lõi: Linux, Bash Script, Docker, Git, C++ và Python.

---

## 🛠️ 2. Tech Stack & Phân công Kỹ thuật
1. **Git:** Bắt sự kiện tự động khi lập trình viên gõ `git push` thông qua Git Hooks (`pre-push`).
2. **Python (Core Engine):** Đọc & phân tích cấu hình `.ci-pipeline.yaml`, điều khiển thứ tự các Stage (`lint`, `test`, `build`), tương tác với Docker SDK qua Unix Socket.
3. **Docker:** Khởi tạo các Ephemeral Container tạm thời (`docker run --rm`) để chạy các lệnh build/test trong môi trường cô lập, sau đó đóng gói ứng dụng thành phẩm.
4. **C++ (Performance Monitor):** Đọc trực tiếp mức tiêu thụ RAM/CPU của Container từ Linux Cgroups v2 (`/sys/fs/cgroup/`) và stream log thời gian thực với màu sắc ANSI trực quan.
5. **Bash Script:** Tự động hóa việc nén Artifacts (`.tar.gz`), dọn dẹp thư mục tạm `/tmp` và viết script cài đặt 1-click `install.sh`.
6. **Linux:** Quản lý tiến trình (POSIX signals), phân quyền hệ thống và tích hợp dịch vụ chạy ngầm với Linux Systemd.

---

## 📂 3. Cấu trúc Cây Thư mục Dự án
```text
lightweight-ci-runner/
├── bin/                          # Chứa file binary C++ biên dịch (ci-monitor)
│   └── .gitkeep
├── src/                          # Mã nguồn chính
│   ├── engine.py                 # [Python] Lõi điều khiển CI & Docker
│   ├── parser.py                 # [Python] Đọc & kiểm tra file YAML
│   └── monitor.cpp               # [C++] Đo RAM/CPU Cgroups & Stream log
├── scripts/                      # Script Bash tự động hóa
│   ├── pre-push                  # [Bash] Git Hook tự động kích hoạt CI
│   ├── deploy.sh                 # [Bash] Nén Artifacts & cập nhật App
│   └── cleanup.sh                # [Bash] Dọn dẹp container rác
├── systemd/
│   └── lightweight-ci.service    # File cấu hình Linux Systemd service
├── sample-app/                   # App mẫu để kiểm thử CI Engine
│   ├── app.py                    # Code Python của app
│   ├── test_app.py               # Unit tests (pytest)
│   ├── Dockerfile                # Dockerfile của app mẫu
│   └── .ci-pipeline.yaml         # Cấu hình pipeline mẫu
├── install.sh                    # Script cài đặt 1-click tự động
├── Makefile                      # Lệnh make build, make clean
├── requirements.txt              # Thư viện Python (pyyaml, docker, rich)
├── .gitignore                    # Bỏ qua file rác
├── LICENSE                       # MIT License
└── README.md                     # Tài liệu kiến trúc dự án
```

---

## 🗺️ 4. Lộ trình 5 Bước Triển khai (Chuẩn Gitflow)

1. **Bước 1 (Nhánh `feat/project-setup`):** 
   - Khởi tạo khung thư mục, viết `.gitignore`, `requirements.txt`, `Makefile`, `bin/.gitkeep`.
2. **Bước 2 (Nhánh `feat/sample-app`):** 
   - Xây dựng ứng dụng Python mẫu (`sample-app/app.py`, `test_app.py`, `Dockerfile`, `.ci-pipeline.yaml`) làm vật thí nghiệm cho CI Engine.
3. **Bước 3 (Nhánh `feat/core-engine`):** 
   - Lập trình bộ não Python (`src/parser.py`, `src/engine.py`) để đọc YAML và điều khiển Docker Container chạy các bước test/build.
4. **Bước 4 (Nhánh `feat/cpp-monitor`):** 
   - Viết module C++ (`src/monitor.cpp`) đọc dữ liệu Cgroups v2 và stream log thời gian thực, cập nhật `Makefile`.
5. **Bước 5 (Nhánh `feat/gitops-automation`):** 
   - Viết các script Bash (`scripts/pre-push`, `deploy.sh`, `cleanup.sh`) và hoàn thiện `install.sh`.
6. **Bước 6:** Gộp (Merge) vào nhánh `main`, cập nhật `README.md` và tạo Release `v1.0.0`.

---

## 🎯 Yêu cầu tiếp theo khi bắt đầu phiên mới:
- Bắt đầu thực hiện **BƯỚC 1: Khởi tạo nhánh `feat/project-setup`**, tạo khung dự án và viết chi tiết nội dung các file: `.gitignore`, `requirements.txt`, `Makefile`.
