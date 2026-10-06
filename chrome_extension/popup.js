/**
 * popup.js - Blogger AI Studio Booster
 */

const STUDIO_URL = "http://127.0.0.1:8888";

document.addEventListener("DOMContentLoaded", async () => {
  const studioStatus = document.getElementById("studioStatus");
  const draftStatus = document.getElementById("draftStatus");
  const tabType = document.getElementById("tabType");
  const blogIdRow = document.getElementById("blogIdRow");
  const blogIdVal = document.getElementById("blogIdVal");
  const msgBox = document.getElementById("msgBox");

  const btnFillDraft = document.getElementById("btnFillDraft");
  const btnExtractToStudio = document.getElementById("btnExtractToStudio");
  const btnAddBlogToStudio = document.getElementById("btnAddBlogToStudio");
  const btnOpenStudio = document.getElementById("btnOpenStudio");
  const btnOpenBlogger = document.getElementById("btnOpenBlogger");

  let currentDraft = null;
  let activeTab = null;
  let activeBlogId = null;
  let isEditorMode = false;

  function showMessage(text, type = "success") {
    msgBox.textContent = text;
    msgBox.className = `msg-box ${type}`;
  }

  // 1. Check Studio Connection & Current Draft
  async function checkStudio() {
    try {
      const res = await fetch(`${STUDIO_URL}/api/draft`, { cache: "no-store" });
      const data = await res.json();
      if (data.success && data.draft) {
        currentDraft = data.draft;
        studioStatus.innerHTML = `<span class="dot green"></span> Sẵn sàng (Port 8888)`;
        
        const titleShort = currentDraft.title 
          ? (currentDraft.title.length > 25 ? currentDraft.title.slice(0, 25) + "..." : currentDraft.title)
          : "Chưa có tiêu đề";
        draftStatus.innerHTML = `<b style="color:#a5b4fc;">${titleShort}</b>`;
        return true;
      }
    } catch (e) {
      studioStatus.innerHTML = `<span class="dot red"></span> Chưa bật Studio Server`;
      draftStatus.textContent = "Chưa kết nối";
    }
    return false;
  }

  // 2. Inspect Active Tab
  async function inspectTab() {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tabs || tabs.length === 0) return;
    activeTab = tabs[0];
    const url = activeTab.url || "";

    if (url.includes("blogger.com")) {
      // Extract Blog ID from URL
      // Formats: /blog/pages/1444..., /blog/post/edit/1444.../..., /blog/page/edit/1444.../...
      const match = url.match(/blog\/(?:pages|posts|page|post|settings|themes|layout|stats|comments)\/(?:edit\/)?([0-9]+)/);
      if (match && match[1]) {
        activeBlogId = match[1];
        blogIdRow.style.display = "flex";
        blogIdVal.textContent = activeBlogId;
        btnAddBlogToStudio.style.display = "flex";
      }

      if (url.includes("/edit/") || url.includes("/post/create") || url.includes("/page/create")) {
        isEditorMode = true;
        tabType.innerHTML = `<span class="dot green"></span> Đang mở Trình Soạn Thảo`;
        btnFillDraft.disabled = false;
        btnExtractToStudio.style.display = "flex";
      } else {
        tabType.innerHTML = `<span class="dot green"></span> Đang ở Quản Trị Blogger`;
        btnFillDraft.disabled = true;
        btnFillDraft.title = "Vui lòng mở một trang hoặc bài viết cần chỉnh sửa";
      }
    } else {
      tabType.innerHTML = `<span class="dot orange"></span> Chưa mở tab Blogger`;
      btnOpenBlogger.style.display = "flex";
      btnFillDraft.disabled = true;
    }
  }

  // 3. Actions
  btnFillDraft.addEventListener("click", async () => {
    if (!activeTab || !isEditorMode) {
      showMessage("Vui lòng mở tab soạn thảo của Blogger trước!", "warning");
      return;
    }
    if (!currentDraft || !currentDraft.content_html) {
      showMessage("Chưa có bản nháp nào trong Studio! Hãy bấm sinh mã trên Studio trước.", "warning");
      return;
    }

    btnFillDraft.disabled = true;
    btnFillDraft.textContent = "⏳ Đang tự động điền...";

    try {
      chrome.tabs.sendMessage(activeTab.id, {
        action: "FILL_DRAFT",
        draft: currentDraft
      }, (response) => {
        btnFillDraft.disabled = false;
        btnFillDraft.textContent = "⚡ 1-Click Điền Bản Nháp Vào Blogger";
        
        if (chrome.runtime.lastError) {
          // Fallback: inject content script on-the-fly
          chrome.scripting.executeScript({
            target: { tabId: activeTab.id },
            files: ["content.js"]
          }, () => {
            setTimeout(() => {
              chrome.tabs.sendMessage(activeTab.id, {
                action: "FILL_DRAFT",
                draft: currentDraft
              }, (resp2) => {
                if (resp2 && resp2.success) {
                  showMessage("✅ Đã điền Tiêu đề, HTML & Mô tả SEO thành công!", "success");
                } else {
                  showMessage("⚠️ Đã thử điền. Hãy kiểm tra trình soạn thảo Blogger.", "warning");
                }
              });
            }, 300);
          });
        } else if (response && response.success) {
          showMessage("✅ Đã điền xong Tiêu đề, Mã HTML và Mô tả tìm kiếm vào Blogger!", "success");
        } else {
          showMessage(response?.message || "Đã gửi dữ liệu vào trang Blogger.", "success");
        }
      });
    } catch (e) {
      btnFillDraft.disabled = false;
      btnFillDraft.textContent = "⚡ 1-Click Điền Bản Nháp Vào Blogger";
      showMessage("Lỗi: " + e.message, "error");
    }
  });

  btnExtractToStudio.addEventListener("click", async () => {
    if (!activeTab) return;
    btnExtractToStudio.disabled = true;
    btnExtractToStudio.textContent = "⏳ Đang kéo dữ liệu...";

    chrome.tabs.sendMessage(activeTab.id, { action: "EXTRACT_POST" }, async (response) => {
      btnExtractToStudio.disabled = false;
      btnExtractToStudio.textContent = "📥 Kéo Bài Từ Blogger Về Studio Để Tối Ưu";

      if (response && response.success && response.data) {
        try {
          await fetch(`${STUDIO_URL}/api/draft`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(response.data)
          });
          showMessage("✅ Đã đồng bộ bài viết này về Studio Pro thành công!", "success");
        } catch (e) {
          showMessage("Lỗi đồng bộ về Studio: " + e.message, "error");
        }
      } else {
        showMessage("Không tìm thấy nội dung bài viết trong tab này.", "warning");
      }
    });
  });

  btnAddBlogToStudio.addEventListener("click", () => {
    if (!activeBlogId) return;
    // Broadcast or save to local storage
    chrome.storage.local.set({ lastCopiedBlogId: activeBlogId });
    navigator.clipboard.writeText(activeBlogId);
    showMessage(`✅ Đã sao chép Blog ID [${activeBlogId}]. Bạn có thể dán vào Studio!`, "success");
  });

  btnOpenStudio.addEventListener("click", () => {
    chrome.tabs.create({ url: STUDIO_URL });
  });

  btnOpenBlogger.addEventListener("click", () => {
    chrome.tabs.create({ url: "https://www.blogger.com" });
  });

  // Init
  await checkStudio();
  await inspectTab();
});
