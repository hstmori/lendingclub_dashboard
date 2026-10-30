# LendingClub Portfolio & Credit Risk Dashboard

Dashboard Power BI phân tích **rủi ro tín dụng và lợi nhuận** của danh mục cho vay LendingClub giai đoạn **2010–2017** (1,76 triệu khoản vay, 26 tỷ USD giải ngân). Dữ liệu thô 1,3 GB được Python gộp thành một *segment cube* nhẹ (27 MB). Power BI chỉ đọc cube này, nên file nhẹ và refresh nhanh.

**Công cụ:** Python (pandas) · Jupyter · Power BI Desktop (định dạng PBIP, model TMDL) · DAX

<!--
Ảnh chụp dashboard: lưu ảnh vào docs/images/ rồi bỏ comment các dòng dưới.
![Tổng quan](docs/images/01_tong_quan.png)
![Vintage & lợi nhuận](docs/images/03_vintage_loi_nhuan.png)
![Chất lượng vintage](docs/images/04_chat_luong_vintage.png)
![Danh sách hành động](docs/images/05_danh_sach_hanh_dong.png)
-->

## Câu hỏi dashboard trả lời

1. Danh mục lớn cỡ nào, rủi ro vỡ nợ ở đâu (theo Grade, kỳ hạn, mục đích vay, FICO, DTI, thu nhập)?
2. Lãi suất thu được có đủ bù tổn thất, chi phí vốn và chi phí vận hành không?
3. Chất lượng cho vay thay đổi thế nào qua các năm giải ngân (vintage), khi so ở **cùng độ tuổi khoản vay**?
4. Nên thắt chặt, định giá lại hay mở rộng ở những phân khúc nào, và tác động bằng tiền là bao nhiêu?

## Các trang

| Trang | Nội dung |
|---|---|
| **Tổng quan** | KPI danh mục, giải ngân và tỷ lệ vỡ nợ theo vintage, vỡ nợ theo mục đích vay |
| **Phân khúc rủi ro** | Ma trận Grade × Term, FICO × DTI; vỡ nợ theo sở hữu nhà và thu nhập |
| **Vintage & lợi nhuận** | Card USD (lãi, tổn thất, chi phí, contribution), waterfall trên 100 USD giải ngân, APR vs Break-even APR theo Grade |
| **Chất lượng vintage** | Tỷ lệ vỡ nợ sau 12/24/36 tháng, trễ hạn hiện tại, trả sớm, settlement, contribution cận trên/cận dưới |
| **Danh sách hành động** | Khuyến nghị theo phân khúc (Grade × Term × Purpose × FICO × DTI), tác động pro-forma nếu dừng phân khúc lỗ |
| **Phương pháp** | Định nghĩa, giả định và cảnh báo |

Slicer **chi phí vốn** (mặc định 4%/năm) và **chi phí vận hành** (1%/năm) đồng bộ giữa các trang lợi nhuận, dùng để chạy kịch bản.

## Chỉ số chính

| Chỉ số | Cách tính |
|---|---|
| Matured Default Rate (PD) | Default + Charged Off ÷ khoản đã có outcome cuối (Fully Paid / Default / Charged Off) |
| Default Rate 12M / 24M / 36M | Khoản vỡ nợ trong N tháng đầu ÷ khoản đã giải ngân đủ N tháng trước ngày chốt dữ liệu (03/2019), nên so sánh được giữa các vintage |
| Weighted APR | Lãi suất bình quân có trọng số theo số tiền giải ngân |
| Gross Interest | Lãi đã thực thu (`total_rec_int`) |
| Net Credit Loss | Max(giải ngân − gốc đã trả, 0) − recoveries, chỉ với khoản vỡ nợ |
| Balance-Years | Dư nợ bình quân × số năm, suy ra từ lãi đã thu ÷ APR của từng dòng |
| Funding / Operating Cost | Balance-Years × tỷ lệ chi phí |
| **Contribution** | Gross Interest − Net Credit Loss − Funding Cost − Operating Cost |
| Contribution Rate | Contribution ÷ Balance-Years (theo năm) |
| Break-even APR | Tổn thất ròng/năm + chi phí vốn + chi phí vận hành |
| Matured Contribution Margin | Contribution chỉ trên khoản đã đóng (cận dưới; Contribution Margin là cận trên) |

Toàn bộ công thức DAX nằm trong [`Portfolio_Cube.tmdl`](powerbi/LendingClub_Portfolio_Dashboard.SemanticModel/definition/tables/Portfolio_Cube.tmdl).

## Kết quả nổi bật (giả định chi phí mặc định)

- Danh mục lãi đóng góp khoảng **0,58 tỷ USD (2,2% số tiền giải ngân)**. Cứ 100 USD cho vay thì thu 18,9 USD lãi, mất 9,8 USD vì vỡ nợ, 6,9 USD cho chi phí vốn và vận hành.
- Khi so cùng độ tuổi, **chất lượng cho vay xấu dần từ 2013 đến 2016**: PD 12 tháng tăng từ 4,8% lên 6,9%, Contribution Margin giảm từ 6,5% xuống khoảng 0,6%. Năm 2017 có dấu hiệu thắt chặt lại (PD 24 tháng còn 11,0%).
- **Grade B–E** có biên APR so với Break-even khoảng +1,6 đến +2,2 điểm %. **Grade G lãi suất thấp hơn mức hoà vốn**.
- 125 phân khúc đủ dữ liệu đang lỗ, chiếm 9,2% số tiền giải ngân. Dừng các phân khúc này chỉ tăng contribution khoảng 24 triệu USD (+4%), nên **định giá lại** hiệu quả hơn cắt bỏ.

## Cấu trúc repo

```
├── data/raw/                                ← đặt dữ liệu gốc ở đây (không đưa lên Git)
├── scripts/00_filter_2010_2017.py           ← lọc file gốc xuống 2010–2017
├── 01_prepare_lendingclub_dashboard.ipynb   ← kiểm tra chất lượng dữ liệu, tạo segment cube
├── outputs/lendingclub_dashboard/
│   ├── data/lendingclub_segment_cube.csv    ← dữ liệu mà Power BI đọc (132.733 dòng × 37 cột)
│   └── evidence/                            ← QA: số dòng, missing values, trạng thái khoản vay, KPI kiểm chứng
└── powerbi/
    ├── LendingClub_Portfolio_Dashboard.pbip ← mở file này
    ├── LendingClub_Portfolio_Dashboard.Report/
    └── LendingClub_Portfolio_Dashboard.SemanticModel/
```

## Cách chạy lại

**Chỉ xem dashboard:** cube đã có sẵn trong repo, nên bỏ qua bước 1–3.

1. Tải `accepted_2007_to_2018Q4.csv` từ Kaggle ([LendingClub Loan Data](https://www.kaggle.com/datasets/wordsforthewise/lending-club)) vào `data/raw/`.
2. Cài thư viện, rồi lọc dữ liệu (chạy từ thư mục gốc repo):

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   python scripts/00_filter_2010_2017.py
   ```
3. Chạy notebook để tạo lại cube:

   ```bash
   jupyter nbconvert --to notebook --execute --inplace 01_prepare_lendingclub_dashboard.ipynb
   ```
4. Mở `powerbi/LendingClub_Portfolio_Dashboard.pbip` bằng Power BI Desktop (bản từ 04/2025). Vào **Transform data → Edit parameters**, sửa `DataFolder` thành đường dẫn tới `outputs\lendingclub_dashboard\data\` trên máy bạn (có dấu `\` ở cuối), rồi bấm **Refresh**.

## Giả định & hạn chế

- Chỉ có khoản vay **đã được duyệt**, nên không phân tích được quyết định duyệt/từ chối.
- LGD, EAD, recovery, chi phí và contribution đều là **proxy**: dữ liệu không có số dư thực tế tại thời điểm vỡ nợ. Tháng vỡ nợ được ước tính bằng tháng trả tiền cuối cùng.
- **Maturity bias:** vintage 2016–2017 còn nhiều khoản đang trả. Hãy xem kèm `Maturity Coverage` và các chỉ số 12/24/36M. Contribution của vintage non được trình bày dưới dạng khoảng: cận trên là mọi khoản, cận dưới là chỉ khoản đã đóng.
- Chi phí vốn và chi phí vận hành là **giả định**, không lấy từ dữ liệu LendingClub.
- Các biến phát sinh sau giải ngân (`loan_status`, `total_pymnt`, `recoveries`…) chỉ dùng để đo kết quả, không dùng được cho mô hình duyệt vay.

## Nguồn dữ liệu

LendingClub accepted loans 2007–2018Q4, bản công khai trên Kaggle. Repo không phân phối lại dữ liệu gốc, chỉ chứa bảng tổng hợp.
