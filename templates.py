"""
templates.py - LuViet Blogger Component & Content Generator Engine
Tạo mã HTML chuẩn Blogger, phong cách LuViet gradient, responsive Mobile/Tablet, tích hợp Schema và Internal Links.
"""

import json

LUVIET_GRADIENT = "linear-gradient(135deg, #6d3990 0%, #d43434 50%, #032690 100%)"
LUVIET_GRADIENT_SOFT = "linear-gradient(135deg, rgba(109,57,144,0.08) 0%, rgba(212,52,52,0.05) 50%, rgba(3,38,144,0.08) 100%)"
LUVIET_GRADIENT_DARK = "linear-gradient(135deg, #1e1b4b 0%, #2e1065 50%, #032690 100%)"

BASE_CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    .lv-service-wrapper {
      --lv-gradient: linear-gradient(135deg, #6d3990 0%, #d43434 50%, #032690 100%);
      --lv-gradient-soft: linear-gradient(135deg, rgba(109,57,144,0.08) 0%, rgba(212,52,52,0.05) 50%, rgba(3,38,144,0.08) 100%);
      --lv-gradient-dark: linear-gradient(135deg, #1e1b4b 0%, #2e1065 50%, #032690 100%);
      --lv-purple: #6d3990;
      --lv-red: #d43434;
      --lv-navy: #032690;
      --lv-zalo: #0068ff;
      --lv-green: #22c55e;
      --lv-dark: #1e293b;
      --lv-text: #334155;
      --lv-text-muted: #64748b;
      --lv-bg-light: #f8fafc;
      --lv-card-bg: #ffffff;
      --lv-border: #e2e8f0;
      --lv-shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
      --lv-shadow-md: 0 10px 25px -3px rgba(109, 57, 144, 0.08);
      --lv-shadow-lg: 0 20px 35px -5px rgba(109, 57, 144, 0.15);
      --lv-radius-sm: 10px;
      --lv-radius-md: 16px;
      --lv-radius-lg: 24px;
      
      font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: var(--lv-text);
      line-height: 1.7;
      font-size: 16px;
      width: 100%;
      max-width: 1140px;
      margin: 15px auto 40px auto;
      box-sizing: border-box;
    }

    .lv-service-wrapper * {
      box-sizing: border-box;
    }

    /* HERO CARD */
    .lv-hero-card {
      background: var(--lv-gradient);
      color: #ffffff;
      border-radius: var(--lv-radius-lg);
      padding: 45px 35px;
      position: relative;
      overflow: hidden;
      box-shadow: var(--lv-shadow-lg);
      margin-bottom: 35px;
      text-align: center;
    }

    .lv-hero-card::before {
      content: '';
      position: absolute;
      top: -40%;
      right: -20%;
      width: 480px;
      height: 480px;
      background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 70%);
      border-radius: 50%;
      pointer-events: none;
    }

    .lv-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.22);
      backdrop-filter: blur(10px);
      padding: 7px 20px;
      border-radius: 50px;
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 18px;
      border: 1px solid rgba(255, 255, 255, 0.35);
    }

    .lv-hero-card h2 {
      font-size: 32px;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 16px 0;
      line-height: 1.35;
    }

    .lv-hero-card p {
      font-size: 17px;
      color: rgba(255, 255, 255, 0.95);
      max-width: 860px;
      margin: 0 auto 26px auto;
      line-height: 1.65;
    }

    .lv-hero-chips {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
    }

    .lv-hero-chip {
      background: rgba(255, 255, 255, 0.16);
      backdrop-filter: blur(6px);
      padding: 8px 18px;
      border-radius: 30px;
      font-size: 14px;
      font-weight: 600;
      border: 1px solid rgba(255, 255, 255, 0.28);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* SECTION HEADERS */
    .lv-section-header {
      text-align: center;
      margin: 45px 0 28px 0;
    }

    .lv-section-header h3 {
      font-size: 26px;
      font-weight: 800;
      color: var(--lv-dark);
      margin: 0 0 10px 0;
      position: relative;
      display: inline-block;
    }

    .lv-section-header h3::after {
      content: '';
      display: block;
      width: 60px;
      height: 4px;
      background: var(--lv-gradient);
      border-radius: 2px;
      margin: 8px auto 0 auto;
    }

    .lv-section-header p {
      font-size: 15.5px;
      color: var(--lv-text-muted);
      max-width: 720px;
      margin: 0 auto;
    }

    /* FEATURES GRID */
    .lv-features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 22px;
      margin-bottom: 40px;
    }

    .lv-feature-card {
      background: var(--lv-card-bg);
      border-radius: var(--lv-radius-md);
      border: 1px solid var(--lv-border);
      padding: 24px 20px;
      box-shadow: var(--lv-shadow-sm);
      transition: all 0.3s ease;
      display: flex;
      flex-direction: column;
    }

    .lv-feature-card:hover {
      transform: translateY(-5px);
      box-shadow: var(--lv-shadow-lg);
      border-color: var(--lv-purple);
    }

    .lv-feature-icon {
      width: 50px;
      height: 50px;
      border-radius: 14px;
      background: var(--lv-gradient-soft);
      color: var(--lv-purple);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      margin-bottom: 16px;
    }

    .lv-feature-card h4 {
      font-size: 17px;
      font-weight: 700;
      color: var(--lv-dark);
      margin: 0 0 8px 0;
      line-height: 1.4;
    }

    .lv-feature-card p {
      font-size: 14px;
      color: var(--lv-text-muted);
      margin: 0;
      line-height: 1.55;
      flex-grow: 1;
    }

    /* PRICING GRID */
    .lv-pricing-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 45px;
      align-items: stretch;
    }

    .lv-pricing-card {
      background: var(--lv-card-bg);
      border-radius: var(--lv-radius-md);
      border: 1px solid var(--lv-border);
      padding: 32px 26px;
      box-shadow: var(--lv-shadow-sm);
      display: flex;
      flex-direction: column;
      position: relative;
      transition: all 0.3s ease;
    }

    .lv-pricing-card:hover {
      box-shadow: var(--lv-shadow-lg);
      transform: translateY(-4px);
    }

    .lv-pricing-card.featured {
      border: 2px solid var(--lv-purple);
      background: linear-gradient(180deg, #ffffff 0%, #faf5ff 100%);
      box-shadow: var(--lv-shadow-md);
    }

    .lv-pricing-badge {
      position: absolute;
      top: -14px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--lv-gradient);
      color: #ffffff;
      font-size: 12px;
      font-weight: 800;
      padding: 5px 16px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }

    .lv-pricing-header {
      text-align: center;
      border-bottom: 1px solid var(--lv-border);
      padding-bottom: 20px;
      margin-bottom: 20px;
    }

    .lv-pricing-name {
      font-size: 20px;
      font-weight: 800;
      color: var(--lv-dark);
      margin-bottom: 8px;
    }

    .lv-pricing-price {
      font-size: 32px;
      font-weight: 800;
      color: var(--lv-purple);
      margin-bottom: 4px;
    }

    .lv-pricing-note {
      font-size: 13px;
      color: var(--lv-text-muted);
    }

    .lv-pricing-features {
      list-style: none;
      padding: 0;
      margin: 0 0 25px 0;
      flex-grow: 1;
    }

    .lv-pricing-features li {
      font-size: 14.5px;
      color: var(--lv-text);
      padding: 8px 0;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px dashed rgba(226, 232, 240, 0.7);
    }

    .lv-pricing-features li i.fa-check {
      color: var(--lv-green);
      font-weight: 700;
    }

    .lv-pricing-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 13px 20px;
      border-radius: 10px;
      font-size: 15px;
      font-weight: 700;
      text-decoration: none !important;
      transition: all 0.25s ease;
      text-align: center;
    }

    .lv-btn-primary {
      background: var(--lv-gradient);
      color: #ffffff !important;
      box-shadow: 0 4px 14px rgba(109, 57, 144, 0.25);
    }

    .lv-btn-primary:hover {
      opacity: 0.92;
      transform: translateY(-2px);
    }

    .lv-btn-secondary {
      background: var(--lv-bg-light);
      color: var(--lv-dark) !important;
      border: 1px solid var(--lv-border);
    }

    /* PROCESS TIMELINE */
    .lv-process-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 18px;
      margin-bottom: 40px;
    }

    .lv-process-step {
      background: var(--lv-card-bg);
      border: 1px solid var(--lv-border);
      border-radius: var(--lv-radius-sm);
      padding: 20px 16px;
      text-align: center;
    }

    .lv-process-num {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: var(--lv-gradient);
      color: #ffffff;
      font-weight: 800;
      font-size: 17px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 12px auto;
    }

    .lv-process-step h5 {
      font-size: 15px;
      font-weight: 700;
      color: var(--lv-dark);
      margin: 0 0 6px 0;
    }

    .lv-process-step p {
      font-size: 13.5px;
      color: var(--lv-text-muted);
      margin: 0;
      line-height: 1.45;
    }

    /* PAYMENT BOX */
    .lv-payment-box {
      background: var(--lv-card-bg);
      border: 2px solid #e0e7ff;
      border-radius: var(--lv-radius-md);
      padding: 30px;
      box-shadow: var(--lv-shadow-md);
      margin-bottom: 35px;
      position: relative;
      overflow: hidden;
    }

    .lv-payment-box::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 6px;
      height: 100%;
      background: var(--lv-gradient);
    }

    .lv-payment-grid {
      display: grid;
      grid-template-columns: 1fr 1.3fr;
      gap: 30px;
      align-items: center;
    }

    /* FAQ ACCORDION */
    .lv-faq-list {
      margin-bottom: 40px;
    }

    .lv-faq-item {
      background: var(--lv-card-bg);
      border: 1px solid var(--lv-border);
      border-radius: var(--lv-radius-sm);
      margin-bottom: 12px;
      overflow: hidden;
    }

    .lv-faq-question {
      padding: 18px 22px;
      font-weight: 700;
      font-size: 16px;
      color: var(--lv-dark);
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #ffffff;
      user-select: none;
    }

    .lv-faq-question:hover {
      background: var(--lv-bg-light);
      color: var(--lv-purple);
    }

    .lv-faq-question i {
      transition: transform 0.3s ease;
      color: var(--lv-purple);
    }

    .lv-faq-item.active .lv-faq-question i {
      transform: rotate(180deg);
    }

    .lv-faq-answer {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease, padding 0.3s ease;
      background: #fafafa;
      color: var(--lv-text);
      font-size: 15px;
      line-height: 1.7;
      padding: 0 22px;
    }

    .lv-faq-item.active .lv-faq-answer {
      max-height: 400px;
      padding: 16px 22px 20px 22px;
      border-top: 1px solid var(--lv-border);
    }

    /* CTA BANNER */
    .lv-cta-banner {
      background: var(--lv-gradient-dark);
      border-radius: var(--lv-radius-md);
      padding: 38px 32px;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 25px;
      margin-bottom: 40px;
      box-shadow: var(--lv-shadow-md);
    }

    .lv-cta-info h3 {
      font-size: 23px;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 8px 0;
    }

    .lv-cta-info p {
      font-size: 15px;
      color: rgba(255, 255, 255, 0.88);
      margin: 0;
      max-width: 620px;
    }

    .lv-cta-actions {
      display: flex;
      gap: 12px;
      flex-shrink: 0;
    }

    .lv-btn-zalo {
      background: var(--lv-zalo);
      color: #ffffff !important;
      padding: 12px 22px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 14.5px;
      text-decoration: none !important;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .lv-btn-white {
      background: #ffffff;
      color: var(--lv-navy) !important;
      padding: 12px 22px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 14.5px;
      text-decoration: none !important;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    /* INTERNAL LINKS 3 COLS */
    .lv-internal-grid {
      background: var(--lv-bg-light);
      border: 1px solid var(--lv-border);
      border-radius: var(--lv-radius-md);
      padding: 30px;
      margin-top: 30px;
    }

    .lv-internal-grid h4 {
      font-size: 18px;
      font-weight: 800;
      color: var(--lv-dark);
      margin: 0 0 18px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .lv-link-columns {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }

    .lv-link-col h5 {
      font-size: 15px;
      font-weight: 700;
      color: var(--lv-purple);
      margin: 0 0 10px 0;
    }

    .lv-link-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .lv-link-list li {
      margin-bottom: 8px;
    }

    .lv-link-list a {
      color: var(--lv-text);
      text-decoration: none;
      font-size: 14px;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .lv-link-list a:hover {
      color: var(--lv-red);
      transform: translateX(3px);
    }

    /* RESPONSIVE */
    @media (max-width: 991px) {
      .lv-pricing-grid { grid-template-columns: 1fr; }
      .lv-payment-grid { grid-template-columns: 1fr; }
      .lv-cta-banner { flex-direction: column; text-align: center; }
      .lv-cta-actions { width: 100%; justify-content: center; }
      .lv-link-columns { grid-template-columns: 1fr; }
    }

    @media (max-width: 576px) {
      .lv-hero-card { padding: 32px 20px; }
      .lv-hero-card h2 { font-size: 24px; }
      .lv-hero-card p { font-size: 15px; }
      .lv-cta-actions { flex-direction: column; }
      .lv-btn-zalo, .lv-btn-white { width: 100%; justify-content: center; }
    }
"""

def generate_internal_links_component():
    return """
  <!-- DANH MỤC LIÊN KẾT NỘI BỘ SEO -->
  <div class="lv-internal-grid">
    <h4><i class="fa fa-sitemap" style="color: var(--lv-purple);"></i> Dịch Vụ Thiết Kế &amp; Cẩm Nang Hữu Ích LuViet</h4>
    <div class="lv-link-columns">
      <div class="lv-link-col">
        <h5>Dịch Vụ Trọng Tâm</h5>
        <ul class="lv-link-list">
          <li><a href="https://www.luviet.com/p/thiet-ke-website-tron-goi.html"><i class="fa fa-angle-right"></i> Dịch vụ thiết kế website trọn gói</a></li>
          <li><a href="https://www.luviet.com/p/dich-vu-thiet-ke-website-ban-hang.html"><i class="fa fa-angle-right"></i> Thiết kế web bán hàng chuyên nghiệp</a></li>
          <li><a href="https://www.luviet.com/search/label/khoa-hoc-google-ads"><i class="fa fa-angle-right"></i> Dịch vụ thiết kế web WordPress</a></li>
          <li><a href="https://www.luviet.com/search/label/san-pham"><i class="fa fa-angle-right"></i> Kho mẫu giao diện bán chạy</a></li>
        </ul>
      </div>

      <div class="lv-link-col">
        <h5>Hướng Dẫn Kỹ Thuật</h5>
        <ul class="lv-link-list">
          <li><a href="https://www.luviet.com/p/huong-dan-thiet-ke-website-wordpress.html"><i class="fa fa-angle-right"></i> Hướng dẫn dựng web WordPress theo mẫu</a></li>
          <li><a href="https://www.luviet.com/p/cach-tro-ten-mien.html"><i class="fa fa-angle-right"></i> Cách trỏ tên miền về hosting mới nhất</a></li>
          <li><a href="https://www.luviet.com/p/huong-dan-tai-ve.html"><i class="fa fa-angle-right"></i> Hướng dẫn đặt hàng &amp; tải về mã nguồn</a></li>
          <li><a href="https://www.luviet.com/search/label/kien-thuc-domain-hosting"><i class="fa fa-angle-right"></i> Cẩm nang Domain &amp; Web Hosting</a></li>
        </ul>
      </div>

      <div class="lv-link-col">
        <h5>Hệ Thống Marketing AI</h5>
        <ul class="lv-link-list">
          <li><a href="https://www.luviet.com/p/he-thong-tu-ong-hoa-blogger-ai.html"><i class="fa fa-angle-right"></i> Cỗ máy tự động hóa viết bài Blogger AI</a></li>
          <li><a href="https://my.luviet.com" target="_blank"><i class="fa fa-angle-right"></i> Nền tảng Landing Page AILADI Platform</a></li>
          <li><a href="https://www.luviet.com/search/label/viet-content-thue"><i class="fa fa-angle-right"></i> Bảng giá dịch vụ viết content chuẩn SEO</a></li>
          <li><a href="https://www.luviet.com/search/label/kien-thuc-seo-website"><i class="fa fa-angle-right"></i> Cẩm nang tối ưu SEO Onpage Google</a></li>
        </ul>
      </div>
    </div>
  </div>
"""

def generate_cta_component(title="Liên Hệ Nhận Tư Vấn Trực Tiếp 24/7", desc="Đội ngũ kỹ thuật LuViet sẵn sàng giải đáp thắc mắc và hỗ trợ bạn thiết lập website tối ưu nhất."):
    return f"""
  <!-- CTA BANNER CHỐT KHÁCH -->
  <div class="lv-cta-banner">
    <div class="lv-cta-info">
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
    <div class="lv-cta-actions">
      <a href="https://zalo.me/0914878680" target="_blank" class="lv-btn-zalo"><i class="fa fa-comment"></i> Chat Zalo 0914 87 86 80</a>
      <a href="tel:0914878680" class="lv-btn-white"><i class="fa fa-phone"></i> Gọi Hotline</a>
    </div>
  </div>
"""

def generate_faq_component(faqs):
    faq_items_html = ""
    for i, item in enumerate(faqs):
        active_class = " active" if i == 0 else ""
        faq_items_html += f"""
    <div class="lv-faq-item{active_class}">
      <div class="lv-faq-question" onclick="this.parentElement.classList.toggle('active')">
        <span>{i+1}. {item['q']}</span>
        <i class="fa fa-chevron-down"></i>
      </div>
      <div class="lv-faq-answer">
        {item['a']}
      </div>
    </div>
"""
    return f"""
  <!-- BỘ CÂU HỎI THƯỜNG GẶP (FAQ) -->
  <div class="lv-section-header">
    <h3>Câu Hỏi Thường Gặp</h3>
    <p>Giải đáp nhanh những thắc mắc phổ biến của khách hàng</p>
  </div>
  <div class="lv-faq-list">
    {faq_items_html}
  </div>
"""

def generate_seo_description(title, keywords=None, page_type="service", content_html=""):
    """
    Tự động sinh mô tả tìm kiếm (Search Description) chuẩn SEO Google & Blogger (130 - 148 ký tự).
    Chứa từ khóa chính, lợi ích cốt lõi và lời kêu gọi hành động (CTA) kích thích CTR.
    Không bị ngắt cụt chữ giữa chừng, đảm bảo câu văn hoàn chỉnh và tự nhiên.
    """
    clean_title = title.strip().replace('"', '').replace("'", "")
    
    if page_type == "sales":
        benefit = "giao diện bán hàng chuẩn CRO, tích hợp VietQR và chuẩn SEO Top Google."
        cta = "Xem ngay ưu đãi LuViet!"
    elif page_type == "guide":
        benefit = "hướng dẫn từng bước từ A-Z, thao tác chuẩn kỹ thuật và dễ hiểu."
        cta = "Khám phá cẩm nang ngay!"
    elif page_type == "article":
        benefit = "phân tích chuyên sâu, bí quyết thực chiến và giải pháp chuẩn SEO."
        cta = "Xem bài viết chi tiết!"
    else:  # service
        benefit = "chuẩn SEO Top Google, tốc độ cao, tương thích di động hoàn hảo."
        cta = "Hotline/Zalo 0914878680 tư vấn ngay!"

    # Thử ráp câu đầy đủ
    desc = f"{clean_title}: {benefit.capitalize()} {cta}"
    
    # Nếu vượt quá 148 ký tự, rút ngắn tiêu đề theo ranh giới từ nguyên vẹn
    if len(desc) > 148:
        max_title_len = 148 - len(f": {benefit.capitalize()} {cta}")
        if max_title_len >= 20:
            words = clean_title.split()
            trunc_title = ""
            for w in words:
                if len(trunc_title + " " + w) <= max_title_len - 3:
                    trunc_title = (trunc_title + " " + w).strip()
                else:
                    break
            desc = f"{trunc_title}...: {benefit.capitalize()} {cta}"
        else:
            # Rút gọn câu ngắn
            desc = f"{clean_title[:50].rsplit(' ', 1)[0]}...: Chuẩn SEO Top Google, giao diện di động mượt mà. Hotline/Zalo 0914878680!"

    if len(desc) > 150:
        desc = desc[:147].rsplit(" ", 1)[0] + "..."
        
    return desc

def generate_page_or_post(page_type, title, keywords=None, outline_items=None):
    """
    Tạo nội dung HTML trọn gói chuẩn Blogger theo từng loại hình trang/bài viết.
    page_type: 'service' | 'guide' | 'sales' | 'article'
    """
    chips_html = ""
    if keywords:
        for kw in keywords[:4]:
            chips_html += f'      <div class="lv-hero-chip"><i class="fa fa-check-circle"></i> {kw.strip()}</div>\n'
    else:
        chips_html = '''      <div class="lv-hero-chip"><i class="fa fa-bolt"></i> Tốc Độ Tải Siêu Tốc &lt; 1.5s</div>
      <div class="lv-hero-chip"><i class="fa fa-mobile"></i> Chuẩn Responsive Mobile &amp; Tablet</div>
      <div class="lv-hero-chip"><i class="fa fa-google"></i> Cấu Trúc Chuẩn SEO Top Google</div>
'''

    if page_type == 'sales':
        badge_text = "Giải Pháp Kinh Doanh Online Đột Phá 2026"
        sub_text = "Xây dựng hệ thống bán hàng trực tuyến chuẩn nhận diện thương hiệu, tích hợp thanh toán tự động, tối ưu trải nghiệm mua sắm trên Mobile & Tablet giúp bùng nổ doanh số."
        body_content = f"""
  <!-- SECTION TÍNH NĂNG ĐỘT PHÁ -->
  <div class="lv-section-header">
    <h3>Các Tính Năng Vượt Trội Tích Hợp Sẵn</h3>
    <p>Mang lại trải nghiệm mua hàng mượt mà và tối ưu hóa tỷ lệ chuyển đổi đơn hàng</p>
  </div>

  <div class="lv-features-grid">
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-mobile-phone"></i></div>
      <h4>Giao Diện Mobile-First</h4>
      <p>Tương thích mượt mà mọi kích cỡ màn hình di động, thao tác vuốt chạm thêm giỏ hàng tự nhiên như App.</p>
    </div>
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-qrcode"></i></div>
      <h4>Thanh Toán VietQR Tự Động</h4>
      <p>Quét mã VietQR tự khớp số tiền và nội dung đơn hàng, hỗ trợ COD, Momo, VNPAY tiện lợi.</p>
    </div>
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-line-chart"></i></div>
      <h4>Chuẩn SEO Onpage Top Google</h4>
      <p>Khai báo Schema Product, Breadcrumbs, tối ưu thẻ Heading và tốc độ tải trang dưới 1.5s.</p>
    </div>
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-bell-o"></i></div>
      <h4>Báo Đơn Hàng Tức Thì</h4>
      <p>Gửi thông báo chốt đơn ngay lập tức qua Email, Zalo hoặc Telegram để bạn chăm sóc khách hàng tức thời.</p>
    </div>
  </div>

  <!-- BẢNG BÁO GIÁ DỊCH VỤ -->
  <div class="lv-section-header">
    <h3>Bảng Giá Dịch Vụ Trọn Gói</h3>
    <p>Chi phí minh bạch 100% - Không phát sinh chi phí ẩn - Bàn giao trọn đời</p>
  </div>

  <div class="lv-pricing-grid">
    <div class="lv-pricing-card">
      <div class="lv-pricing-header">
        <div class="lv-pricing-name">Gói Khởi Nghiệp</div>
        <div class="lv-pricing-price">2.500.000đ</div>
        <div class="lv-pricing-note">Phù hợp shop nhỏ, cá nhân mới bắt đầu kinh doanh</div>
      </div>
      <ul class="lv-pricing-features">
        <li><i class="fa fa-check"></i> Giao diện Blogger hoặc WordPress chuẩn</li>
        <li><i class="fa fa-check"></i> Đầy đủ giỏ hàng &amp; đặt hàng nhanh</li>
        <li><i class="fa fa-check"></i> Tối ưu tương thích di động 100%</li>
        <li><i class="fa fa-check"></i> Tặng tên miền quốc tế (.com) 1 năm</li>
        <li><i class="fa fa-check"></i> Bàn giao trong 3 ngày làm việc</li>
      </ul>
      <a href="https://zalo.me/0914878680?text=TuVanGoiKhoiNghiep" target="_blank" class="lv-pricing-btn lv-btn-secondary">
        <i class="fa fa-hand-o-right"></i> Chọn Gói Này
      </a>
    </div>

    <div class="lv-pricing-card featured">
      <span class="lv-pricing-badge">Được Chọn Nhiều Nhất</span>
      <div class="lv-pricing-header">
        <div class="lv-pricing-name">Gói Chuyên Nghiệp</div>
        <div class="lv-pricing-price">4.500.000đ</div>
        <div class="lv-pricing-note">Dành cho cửa hàng kinh doanh bài bản bứt phá doanh số</div>
      </div>
      <ul class="lv-pricing-features">
        <li><i class="fa fa-check"></i> Thiết kế độc quyền theo nhận diện thương hiệu</li>
        <li><i class="fa fa-check"></i> 1-Click Fast Checkout + Quét VietQR tự động</li>
        <li><i class="fa fa-check"></i> Tặng Tên miền .com + Hosting NVMe Siêu Tốc 1 năm</li>
        <li><i class="fa fa-check"></i> Báo đơn hàng tức thì qua Zalo / Telegram</li>
        <li><i class="fa fa-check"></i> Tối ưu SEO Onpage chuyên sâu Top Google</li>
        <li><i class="fa fa-check"></i> Hỗ trợ kỹ thuật 24/7 trọn đời</li>
      </ul>
      <a href="https://zalo.me/0914878680?text=TuVanGoiChuyenNghiep" target="_blank" class="lv-pricing-btn lv-btn-primary">
        <i class="fa fa-star"></i> Chọn Gói Này
      </a>
    </div>

    <div class="lv-pricing-card">
      <div class="lv-pricing-header">
        <div class="lv-pricing-name">Gói Doanh Nghiệp VIP</div>
        <div class="lv-pricing-price">7.500.000đ</div>
        <div class="lv-pricing-note">Giải pháp sàn E-Commerce đa ngành, tính năng nâng cao</div>
      </div>
      <ul class="lv-pricing-features">
        <li><i class="fa fa-check"></i> UI/UX may đo riêng biệt theo yêu cầu</li>
        <li><i class="fa fa-check"></i> Tích hợp full cổng: Visa, VNPAY, Momo, COD</li>
        <li><i class="fa fa-check"></i> Hệ thống phân quyền đại lý &amp; Coupon VIP</li>
        <li><i class="fa fa-check"></i> Tặng Tên miền .vn + Hosting NVMe Cloud 1 năm</li>
        <li><i class="fa fa-check"></i> Bảo hành &amp; backup dữ liệu hàng ngày</li>
      </ul>
      <a href="https://zalo.me/0914878680?text=TuVanGoiVIP" target="_blank" class="lv-pricing-btn lv-btn-secondary">
        <i class="fa fa-diamond"></i> Chọn Gói VIP
      </a>
    </div>
  </div>
"""
    elif page_type == 'guide':
        badge_text = "Cẩm Nang Hướng Dẫn Kỹ Thuật Chi Tiết Từ A-Z"
        sub_text = "Tài liệu thực hành từng bước trực quan, dễ hiểu giúp bạn nhanh chóng làm chủ kỹ thuật và vận hành hệ thống trơn tru."
        body_content = f"""
  <!-- QUY TRÌNH HƯỚNG DẪN 4 BƯỚC -->
  <div class="lv-section-header">
    <h3>Lộ Trình Triển Khai Từng Bước</h3>
    <p>Thực hiện lần lượt theo các bước hướng dẫn bên dưới để đạt kết quả chuẩn xác nhất</p>
  </div>

  <div class="lv-process-grid">
    <div class="lv-process-step">
      <div class="lv-process-num">01</div>
      <h5>Chuẩn Bị Tài Nguyên</h5>
      <p>Kiểm tra thông tin tài khoản, file mã nguồn và môi trường cài đặt cần thiết.</p>
    </div>
    <div class="lv-process-step">
      <div class="lv-process-num">02</div>
      <h5>Thiết Lập Cấu Hình</h5>
      <p>Nhập thông số kỹ thuật, cấu hình bản ghi hệ thống hoặc import file mẫu.</p>
    </div>
    <div class="lv-process-step">
      <div class="lv-process-num">03</div>
      <h5>Kiểm Tra Vận Hành</h5>
      <p>Chạy thử nghiệm trên các trình duyệt và thiết bị khác nhau để đảm bảo ổn định.</p>
    </div>
    <div class="lv-process-step">
      <div class="lv-process-num">04</div>
      <h5>Bàn Giao &amp; Tối Ưu</h5>
      <p>Hoàn tất thiết lập, tiến hành khai báo Google Search Console và tối ưu SEO.</p>
    </div>
  </div>
"""
    else:
        badge_text = "Dịch Vụ Chuyên Nghiệp - Uy Tín Hàng Đầu Tại LuViet"
        sub_text = "Giải pháp công nghệ và truyền thông số toàn diện giúp doanh nghiệp xây dựng thương hiệu vững mạnh và gia tăng khách hàng tiềm năng."
        body_content = f"""
  <!-- SECTION NỘI DUNG DỊCH VỤ -->
  <div class="lv-section-header">
    <h3>Tại Sao Khách Hàng Luôn Tin Chọn LuViet?</h3>
    <p>Cam kết chất lượng thực tế, đồng hành dài lâu cùng sự phát triển của bạn</p>
  </div>

  <div class="lv-features-grid">
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-code"></i></div>
      <h4>Mã Nguồn Chuẩn Sạch 100%</h4>
      <p>Không chèn mã độc hay link ẩn, tối ưu Core Web Vitals giúp website luôn đạt điểm xanh Google PageSpeed.</p>
    </div>
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-paint-brush"></i></div>
      <h4>Giao Diện Hiện Đại &amp; Độc Quyền</h4>
      <p>Phong cách thiết kế tinh tế, màu sắc hài hòa theo bộ nhận diện thương hiệu của từng ngành nghề.</p>
    </div>
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-headphones"></i></div>
      <h4>Hỗ Trợ Kỹ Thuật 24/7</h4>
      <p>Đội ngũ kỹ sư hỗ trợ trực tiếp qua Ultraview / AnyDesk hoặc Zalo mọi lúc khi bạn cần.</p>
    </div>
    <div class="lv-feature-card">
      <div class="lv-feature-icon"><i class="fa fa-shield"></i></div>
      <h4>Cam Kết Bảo Hành Trọn Đời</h4>
      <p>Bảo hành code vĩnh viễn, hướng dẫn sử dụng và cập nhật tính năng định kỳ miễn phí.</p>
    </div>
  </div>
"""

    schema_json = {
        "@context": "https://schema.org",
        "@type": "Article" if page_type in ['article', 'guide'] else "Service",
        "name": title,
        "description": sub_text,
        "provider": {
            "@type": "Organization",
            "name": "LuViet",
            "url": "https://www.luviet.com"
        }
    }
    schema_script = f'<script type="application/ld+json">\n{json.dumps(schema_json, ensure_ascii=False, indent=2)}\n</script>'

    faqs = [
        {"q": "Quy trình triển khai dịch vụ mất bao lâu?", "a": "Thời gian hoàn thành dao động từ 1 - 5 ngày làm việc tùy thuộc vào quy mô và yêu cầu cụ thể của từng dự án."},
        {"q": "Tôi có được hướng dẫn quản trị và cập nhật bài viết không?", "a": "Có! LuViet cung cấp tài liệu chi tiết, video hướng dẫn 1-1 và hỗ trợ kỹ thuật trực tiếp để bạn hoàn toàn làm chủ hệ thống."},
        {"q": "Chính sách bảo hành và hỗ trợ sau bàn giao như thế nào?", "a": "LuViet cam kết bảo hành kỹ thuật trọn đời, hỗ trợ sao lưu dữ liệu và xử lý mọi thắc mắc 24/7 hoàn toàn miễn phí."}
    ]
    faq_html = generate_faq_component(faqs)
    cta_html = generate_cta_component()
    internal_links_html = generate_internal_links_component()

    full_html = f"""<div class="lv-service-wrapper">
  <style>
{BASE_CSS}
  </style>

  {schema_script}

  <!-- HERO SECTION -->
  <div class="lv-hero-card">
    <div class="lv-badge"><i class="fa fa-star"></i> {badge_text}</div>
    <h2>{title}</h2>
    <p>{sub_text}</p>
    <div class="lv-hero-chips">
{chips_html}
    </div>
  </div>

{body_content}

{faq_html}

{cta_html}

{internal_links_html}
</div>
"""
    return full_html
