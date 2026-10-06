/**
 * content.js - Blogger AI Studio Booster Content Script
 * Injected into Blogger pages to enable 1-Click filling and extraction
 */

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "FILL_DRAFT") {
    fillDraftToBlogger(request.draft).then(res => {
      sendResponse(res);
    }).catch(err => {
      sendResponse({ success: false, error: err.message });
    });
    return true; // async response
  }

  if (request.action === "EXTRACT_POST") {
    const data = extractFromBlogger();
    sendResponse({ success: true, data });
    return true;
  }
});

async function fillDraftToBlogger(draft) {
  if (!draft) return { success: false, message: "Không có dữ liệu bản nháp" };

  let filledSteps = [];

  // 1. Fill Title
  if (draft.title) {
    const titleInp = document.querySelector('input[aria-label="Tiêu đề"], input[aria-label="Title"], input[jsname="YPqjbf"]');
    if (titleInp) {
      titleInp.focus();
      titleInp.value = draft.title;
      titleInp.dispatchEvent(new Event('input', { bubbles: true }));
      titleInp.dispatchEvent(new Event('change', { bubbles: true }));
      titleInp.blur();
      filledSteps.push("Tiêu đề");
    }
  }

  // 2. Switch to HTML Mode if currently in Compose Mode
  let cm = document.querySelector(".CodeMirror")?.CodeMirror;
  if (!cm) {
    const modeBtn = document.querySelector('div[aria-label="Chế độ xem Soạn thảo"], div[aria-label="Chế độ xem HTML"], div[jsname="xw1cm"][aria-haspopup="menu"]');
    if (modeBtn) {
      modeBtn.click();
      await new Promise(r => setTimeout(r, 450));
      const htmlOpt = Array.from(document.querySelectorAll('div[role="menuitem"]')).find(el => el.textContent.includes("HTML"));
      if (htmlOpt) {
        htmlOpt.click();
        await new Promise(r => setTimeout(r, 600));
      }
    }
  }

  // 3. Inject HTML into CodeMirror
  cm = document.querySelector(".CodeMirror")?.CodeMirror;
  if (cm && draft.content_html) {
    cm.setValue(draft.content_html);
    cm.save();
    filledSteps.push("Nội dung HTML");
  } else if (draft.content_html) {
    // Fallback: try contenteditable body
    const editBody = document.querySelector('div[contenteditable="true"]');
    if (editBody) {
      editBody.innerHTML = draft.content_html;
      editBody.dispatchEvent(new Event('input', { bubbles: true }));
      filledSteps.push("Nội dung Soạn Thảo");
    }
  }

  // 4. Fill Search Description (Mô tả tìm kiếm)
  if (draft.search_desc) {
    const cleanDesc = draft.search_desc.trim().slice(0, 150);
    const sideBtns = Array.from(document.querySelectorAll('div[jsname="HSrbLb"]'));
    const descBtn = sideBtns.find(b => b.textContent && (b.textContent.includes("Mô tả tìm kiếm") || b.textContent.includes("Search description")));
    
    if (descBtn) {
      if (descBtn.getAttribute('aria-expanded') !== 'true') {
        descBtn.click();
        await new Promise(r => setTimeout(r, 300));
      }
      const regionId = descBtn.getAttribute('aria-controls') || 'c12';
      const region = document.getElementById(regionId) || descBtn.closest('.mT05K');
      const ta = region ? region.querySelector('textarea') : null;
      if (ta) {
        ta.focus();
        ta.value = cleanDesc;
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        ta.blur();
        filledSteps.push("Mô tả SEO");
      }
    } else {
      const fallbackTa = document.querySelector('textarea[aria-label*="mô tả tìm kiếm" i], textarea[aria-label*="Search description" i]');
      if (fallbackTa) {
        fallbackTa.focus();
        fallbackTa.value = cleanDesc;
        fallbackTa.dispatchEvent(new Event('input', { bubbles: true }));
        fallbackTa.dispatchEvent(new Event('change', { bubbles: true }));
        fallbackTa.blur();
        filledSteps.push("Mô tả SEO");
      }
    }
  }

  // 5. Fill Labels (Nhãn) if available
  if (draft.labels && draft.labels.length > 0) {
    const labelsStr = Array.isArray(draft.labels) ? draft.labels.join(", ") : draft.labels;
    const sideBtns = Array.from(document.querySelectorAll('div[jsname="HSrbLb"]'));
    const lblBtn = sideBtns.find(b => b.textContent && (b.textContent.includes("Nhãn") || b.textContent.includes("Labels")));
    
    if (lblBtn) {
      if (lblBtn.getAttribute('aria-expanded') !== 'true') {
        lblBtn.click();
        await new Promise(r => setTimeout(r, 300));
      }
      const regionId = lblBtn.getAttribute('aria-controls') || 'c8';
      const region = document.getElementById(regionId) || lblBtn.closest('.mT05K');
      const ta = region ? region.querySelector('textarea') : null;
      if (ta) {
        ta.focus();
        ta.value = labelsStr;
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        ta.blur();
        filledSteps.push("Nhãn phân loại");
      }
    }
  }

  // Visual notification on page
  showInPageToast(`Đã điền thành công: ${filledSteps.join(", ")}!`);

  return {
    success: true,
    message: `Đã điền: ${filledSteps.join(", ")}`,
    steps: filledSteps
  };
}

function extractFromBlogger() {
  const titleInp = document.querySelector('input[aria-label="Tiêu đề"], input[aria-label="Title"], input[jsname="YPqjbf"]');
  const title = titleInp ? titleInp.value : "";

  const cm = document.querySelector(".CodeMirror")?.CodeMirror;
  let content_html = "";
  if (cm) {
    content_html = cm.getValue();
  } else {
    const editBody = document.querySelector('div[contenteditable="true"]');
    content_html = editBody ? editBody.innerHTML : "";
  }

  let search_desc = "";
  const sideBtns = Array.from(document.querySelectorAll('div[jsname="HSrbLb"]'));
  const descBtn = sideBtns.find(b => b.textContent && (b.textContent.includes("Mô tả tìm kiếm") || b.textContent.includes("Search description")));
  if (descBtn) {
    const regionId = descBtn.getAttribute('aria-controls') || 'c12';
    const region = document.getElementById(regionId) || descBtn.closest('.mT05K');
    const ta = region ? region.querySelector('textarea') : null;
    if (ta) search_desc = ta.value;
  }

  showInPageToast("Đã trích xuất nội dung từ Blogger về Studio!");

  return {
    title,
    content_html,
    search_desc,
    target_type: window.location.href.includes("/page/") ? "page" : "post"
  };
}

function showInPageToast(msg) {
  let toast = document.getElementById("bloggerStudioBoosterToast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "bloggerStudioBoosterToast";
    toast.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999999;
      background: linear-gradient(135deg, #1e1b4b, #312e81);
      border: 1px solid #6366f1;
      color: #ffffff;
      padding: 12px 18px;
      border-radius: 10px;
      font-size: 13.5px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      transition: all 0.3s ease;
    `;
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<span style="font-size:16px;">⚡</span> <b>Blogger AI Studio:</b> <span>${msg}</span>`;
  toast.style.opacity = "1";
  toast.style.transform = "translateY(0)";

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(15px)";
  }, 3500);
}
