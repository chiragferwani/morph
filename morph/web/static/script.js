/**
 * morph Web Interface — Frontend JavaScript
 *
 * Handles:
 *   1. Sending scrape requests & updating the scraper UI
 *   2. Drag-and-drop file upload for the converter
 *   3. Sending conversion requests using FormData
 *   4. Dynamic output format dropdown updates
 *   5. Displaying results (text, galleries, audio/video players)
 */

// ============================================================
// GLOBAL VARIABLES
// ============================================================
let lastScrapeResult = null;
let lastConvertResult = null;
let downloadFilename = null;
let convertDownloadFilename = null;

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    updateOutputOptions();
    updateConvertOutputOptions();

    // Setup Enter key shortcut for Scraper URL Input
    const urlInput = document.getElementById("url-input");
    if (urlInput) {
        urlInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                startScraping();
            }
        });
    }

    // Setup drag and drop events
    const dropZone = document.getElementById("file-upload-zone");
    if (dropZone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.add('file-selected');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                if (eventName === 'dragleave') {
                    dropZone.classList.remove('file-selected');
                }
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            const fileInput = document.getElementById("convert-file");
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect(fileInput);
            }
        }, false);
    }
});

// ============================================================
// DYNAMIC DROPDOWN OPTION UPDATES
// ============================================================

/**
 * Updates the scraper's output format select box options based on chosen content type.
 */
function updateOutputOptions() {
    const contentType = document.getElementById("content-type").value;
    const outputFormatSelect = document.getElementById("output-format");
    if (!outputFormatSelect) return;

    outputFormatSelect.innerHTML = ""; // Clear existing options

    if (contentType === "text") {
        outputFormatSelect.disabled = false;
        const options = [
            { value: "txt", text: "TXT" },
            { value: "csv", text: "CSV" },
            { value: "json", text: "JSON" }
        ];
        options.forEach(opt => {
            const el = document.createElement("option");
            el.value = opt.value;
            el.textContent = opt.text;
            outputFormatSelect.appendChild(el);
        });
    } else if (contentType === "images") {
        outputFormatSelect.disabled = false;
        const options = [
            { value: "zip", text: "Download All (ZIP)" },
            { value: "jpg", text: "JPG Only" },
            { value: "png", text: "PNG Only" }
        ];
        options.forEach(opt => {
            const el = document.createElement("option");
            el.value = opt.value;
            el.textContent = opt.text;
            outputFormatSelect.appendChild(el);
        });
    } else if (contentType === "audio") {
        outputFormatSelect.disabled = false;
        const options = [
            { value: "zip", text: "Download All (ZIP)" },
            { value: "mp3", text: "MP3 Only" },
            { value: "wav", text: "WAV Only" }
        ];
        options.forEach(opt => {
            const el = document.createElement("option");
            el.value = opt.value;
            el.textContent = opt.text;
            outputFormatSelect.appendChild(el);
        });
    } else if (contentType === "video") {
        outputFormatSelect.disabled = false;
        const options = [
            { value: "zip", text: "Download All (ZIP)" },
            { value: "mp4", text: "MP4 Only" },
            { value: "webm", text: "WEBM Only" }
        ];
        options.forEach(opt => {
            const el = document.createElement("option");
            el.value = opt.value;
            el.textContent = opt.text;
            outputFormatSelect.appendChild(el);
        });
    }
}

/**
 * Updates the converter's output format select options based on chosen conversion type.
 */
function updateConvertOutputOptions() {
    const convType = document.getElementById("conversion-type").value;
    const outputSelect = document.getElementById("convert-output-format");
    if (!outputSelect) return;

    outputSelect.innerHTML = ""; // Clear existing

    if (convType === "image-to-text" || convType === "audio-to-text" || convType === "video-to-text") {
        outputSelect.disabled = false;
        const options = [
            { value: "txt", text: "TXT" },
            { value: "csv", text: "CSV" },
            { value: "json", text: "JSON" }
        ];
        options.forEach(opt => {
            const el = document.createElement("option");
            el.value = opt.value;
            el.textContent = opt.text;
            outputSelect.appendChild(el);
        });
    } else if (convType === "video-to-audio") {
        outputSelect.disabled = true;
        const el = document.createElement("option");
        el.value = "wav";
        el.textContent = "WAV";
        outputSelect.appendChild(el);
    } else if (convType === "video-to-images") {
        outputSelect.disabled = true;
        const el = document.createElement("option");
        el.value = "png";
        el.textContent = "PNG Frames";
        outputSelect.appendChild(el);
    }
}

// ============================================================
// FILE UPLOAD SELECTION HANDLER
// ============================================================
function handleFileSelect(input) {
    const label = document.getElementById("file-upload-label");
    const dropZone = document.getElementById("file-upload-zone");
    if (input.files && input.files.length > 0) {
        const file = input.files[0];
        label.innerHTML = `<span class="file-upload-icon">✅</span><span><strong>Selected:</strong> ${file.name} (${(file.size / 1024).toFixed(1)} KB)</span>`;
        dropZone.classList.add("file-selected");

        // Automatically pre-select conversion type based on extension if not already compatible
        const ext = file.name.split('.').pop().toLowerCase();
        const convType = document.getElementById("conversion-type");
        const currentVal = convType.value;
        if (['jpg', 'jpeg', 'png', 'bmp', 'webp', 'gif'].includes(ext)) {
            if (currentVal !== "image-to-text") {
                convType.value = "image-to-text";
            }
        } else if (['mp3', 'wav', 'ogg', 'flac'].includes(ext)) {
            if (currentVal !== "audio-to-text") {
                convType.value = "audio-to-text";
            }
        } else if (['mp4', 'mov', 'webm', 'avi', 'mkv'].includes(ext)) {
            if (currentVal !== "video-to-audio" && currentVal !== "video-to-text" && currentVal !== "video-to-images") {
                convType.value = "video-to-audio";
            }
        }
        updateConvertOutputOptions();
    } else {
        label.innerHTML = `<span class="file-upload-icon">📁</span><span>Click to choose a file or drag & drop</span>`;
        dropZone.classList.remove("file-selected");
    }
}

// ============================================================
// SCRAPER FLOW
// ============================================================
async function startScraping() {
    const url = document.getElementById("url-input").value.trim();
    const contentType = document.getElementById("content-type").value;
    const outputFormat = document.getElementById("output-format").value;

    if (!url) {
        showScrapeStatus("Please enter a website URL.", "error");
        return;
    }

    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        showScrapeStatus("URL must start with http:// or https://", "error");
        return;
    }

    setScraperLoading(true);
    showScrapeStatus("Scraping started...", "info");
    showProgress(true);
    hideScrapeResults();

    try {
        const response = await fetch("/api/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: url,
                content_type: contentType,
                output_format: outputFormat
            })
        });

        const result = await response.json();

        if (!result.success) {
            showScrapeStatus(`Error: ${result.error}`, "error");
            showProgress(false);
            setScraperLoading(false);
            return;
        }

        lastScrapeResult = result;
        downloadFilename = result.download_file || null;

        displayScrapeResults(contentType, result);
        showScrapeStatus("Scrape completed successfully!", "success");
        showProgress(false);
    } catch (e) {
        showScrapeStatus("Connection failed. Is the backend server running?", "error");
        showProgress(false);
    }
    setScraperLoading(false);
}

function displayScrapeResults(contentType, result) {
    const section = document.getElementById("results-section");
    section.style.display = "block";

    document.getElementById("text-result").style.display = "none";
    document.getElementById("image-result").style.display = "none";
    document.getElementById("audio-result").style.display = "none";
    document.getElementById("video-result").style.display = "none";

    if (contentType === "text") {
        document.getElementById("text-result").style.display = "block";
        document.getElementById("word-count").textContent = `${result.word_count} words`;
        const titleBadge = document.getElementById("page-title");
        if (result.title) {
            titleBadge.textContent = result.title;
            titleBadge.style.display = "inline-block";
        } else {
            titleBadge.style.display = "none";
        }
        document.getElementById("text-content").textContent = result.text;
    } else if (contentType === "images") {
        document.getElementById("image-result").style.display = "block";
        document.getElementById("image-count").textContent = `Found ${result.count} images`;
        const gallery = document.getElementById("image-gallery");
        gallery.innerHTML = "";
        result.images.forEach(img => {
            const item = document.createElement("div");
            item.className = "gallery-item";
            item.innerHTML = `<img src="${img.src}" alt="${img.alt}" loading="lazy"><div class="image-label">${img.filename}</div>`;
            item.onclick = () => window.open(img.src, "_blank");
            gallery.appendChild(item);
        });
    } else if (contentType === "audio") {
        document.getElementById("audio-result").style.display = "block";
        document.getElementById("audio-count").textContent = `Found ${result.count} audio files`;
        const list = document.getElementById("audio-list");
        list.innerHTML = "";
        result.audio_files.forEach(audio => {
            const item = document.createElement("div");
            item.className = "media-item";
            item.innerHTML = `
                <div class="media-item-name">🎵 ${audio.filename}</div>
                <div class="media-item-url">${audio.src}</div>
                <audio controls src="${audio.src}" preload="none"></audio>
            `;
            list.appendChild(item);
        });
    } else if (contentType === "video") {
        document.getElementById("video-result").style.display = "block";
        document.getElementById("video-count").textContent = `Found ${result.count} video files`;
        const list = document.getElementById("video-list");
        list.innerHTML = "";
        result.video_files.forEach(vid => {
            const item = document.createElement("div");
            item.className = "media-item";
            item.innerHTML = `
                <div class="media-item-name">🎬 ${vid.filename}</div>
                <div class="media-item-url">${vid.src}</div>
                <video controls src="${vid.src}" preload="none"></video>
            `;
            list.appendChild(item);
        });
    }

    const dBtn = document.getElementById("download-btn");
    if (contentType === "text") {
        dBtn.style.display = downloadFilename ? "inline-flex" : "none";
    } else {
        const hasItems = (contentType === "images" && result.images && result.images.length > 0) ||
                         (contentType === "audio" && result.audio_files && result.audio_files.length > 0) ||
                         (contentType === "video" && result.video_files && result.video_files.length > 0);
        dBtn.style.display = hasItems ? "inline-flex" : "none";
    }
}

async function downloadResult() {
    const contentType = document.getElementById("content-type").value;
    const outputFormat = document.getElementById("output-format").value;

    if (contentType === "text") {
        if (downloadFilename) {
            window.location.href = `/api/download/${downloadFilename}`;
        }
    } else {
        const dBtn = document.getElementById("download-btn");
        const originalText = dBtn.innerHTML;
        
        dBtn.disabled = true;
        dBtn.innerHTML = `<span class="spinner"></span> Zipping...`;

        try {
            let mediaList = [];
            if (contentType === "images") {
                mediaList = lastScrapeResult.images;
            } else if (contentType === "audio") {
                mediaList = lastScrapeResult.audio_files;
            } else if (contentType === "video") {
                mediaList = lastScrapeResult.video_files;
            }

            const response = await fetch("/api/zip_media", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    content_type: contentType,
                    media: mediaList,
                    output_format: outputFormat
                })
            });

            const result = await response.json();
            if (result.success && result.download_file) {
                window.location.href = `/api/download/${result.download_file}`;
            } else {
                alert("Failed to package files: " + (result.error || "unknown error"));
            }
        } catch (e) {
            alert("Error zipping files.");
        } finally {
            dBtn.disabled = false;
            dBtn.innerHTML = originalText;
        }
    }
}

// ============================================================
// CONVERTER FLOW
// ============================================================
async function startConverting() {
    const fileInput = document.getElementById("convert-file");
    const conversionType = document.getElementById("conversion-type").value;
    const outputFormat = document.getElementById("convert-output-format").value;

    if (!fileInput.files || fileInput.files.length === 0) {
        showConvertStatus("Please upload a file first.", "error");
        return;
    }

    setConverterLoading(true);
    showConvertStatus("Uploading and processing file... This might take a moment.", "info");
    hideConvertResults();

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("conversion_type", conversionType);
    formData.append("output_format", outputFormat);

    try {
        const response = await fetch("/api/convert", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!result.success) {
            showConvertStatus(`Error: ${result.error}`, "error");
            setConverterLoading(false);
            return;
        }

        lastConvertResult = result;
        convertDownloadFilename = result.download_file || null;

        displayConvertResults(conversionType, result);
        showConvertStatus("Conversion completed successfully!", "success");
    } catch (e) {
        showConvertStatus("Connection failed or server error during conversion.", "error");
    }
    setConverterLoading(false);
}

function displayConvertResults(convType, result) {
    const section = document.getElementById("convert-results");
    section.style.display = "block";

    // Hide all panels first
    document.getElementById("convert-text-result").style.display = "none";
    document.getElementById("convert-audio-result").style.display = "none";
    document.getElementById("convert-image-result").style.display = "none";
    document.getElementById("convert-info-result").style.display = "none";

    // Handle text transcription/OCR results
    if (result.text !== undefined) {
        const textPanel = document.getElementById("convert-text-result");
        textPanel.style.display = "block";
        document.getElementById("convert-word-count").textContent = `${result.word_count || 0} words`;
        document.getElementById("convert-text-content").textContent = result.text;
    } 
    // Handle video-to-audio results
    else if (convType === "video-to-audio") {
        const audioPanel = document.getElementById("convert-audio-result");
        audioPanel.style.display = "block";
        const player = document.getElementById("convert-audio-player");
        player.src = `/api/download/${result.download_file}`;
        player.load();

        const infoPanel = document.getElementById("convert-info-result");
        infoPanel.style.display = "block";
        document.getElementById("convert-info-text").innerHTML = `🎵 Extracted audio saved successfully!`;
    }
    // Handle video-to-images results
    else if (convType === "video-to-images") {
        const imagePanel = document.getElementById("convert-image-result");
        imagePanel.style.display = "block";
        document.getElementById("convert-image-count").textContent = `Extracted ${result.count} frames`;

        const gallery = document.getElementById("convert-image-gallery");
        gallery.innerHTML = "";
        result.frames.forEach(frame => {
            const filename = frame.split("/").pop();
            const item = document.createElement("div");
            item.className = "gallery-item";
            item.innerHTML = `<img src="/api/download/${frame}" loading="lazy"><div class="image-label">${filename}</div>`;
            item.onclick = () => window.open(`/api/download/${frame}`, "_blank");
            gallery.appendChild(item);
        });

        const infoPanel = document.getElementById("convert-info-result");
        infoPanel.style.display = "block";
        document.getElementById("convert-info-text").innerHTML = `🖼️ Extracted <strong>${result.count}</strong> frames successfully!`;
    }

    const dBtn = document.getElementById("convert-download-btn");
    dBtn.style.display = convertDownloadFilename ? "inline-flex" : "none";
}

function downloadConvertResult() {
    if (convertDownloadFilename) {
        window.location.href = `/api/download/${convertDownloadFilename}`;
    }
}

// ============================================================
// UI HELPERS
// ============================================================
function setScraperLoading(loading) {
    const btn = document.getElementById("scrape-btn");
    const txt = document.getElementById("scrape-btn-text");
    const loader = document.getElementById("scrape-btn-loader");
    if (loading) {
        txt.style.display = "none";
        loader.style.display = "inline-flex";
        btn.disabled = true;
    } else {
        txt.style.display = "inline-flex";
        loader.style.display = "none";
        btn.disabled = false;
    }
}

function setConverterLoading(loading) {
    const btn = document.getElementById("convert-btn");
    const txt = document.getElementById("convert-btn-text");
    const loader = document.getElementById("convert-btn-loader");
    if (loading) {
        txt.style.display = "none";
        loader.style.display = "inline-flex";
        btn.disabled = true;
    } else {
        txt.style.display = "inline-flex";
        loader.style.display = "none";
        btn.disabled = false;
    }
}

function showScrapeStatus(msg, type) {
    const el = document.getElementById("status-message");
    el.textContent = msg;
    el.className = `status-msg ${type}`;
    el.style.display = "block";
}

function showConvertStatus(msg, type) {
    const el = document.getElementById("convert-status");
    el.textContent = msg;
    el.className = `status-msg ${type}`;
    el.style.display = "block";
}

function showProgress(show) {
    const wrap = document.getElementById("progress-container");
    if (show) {
        wrap.style.display = "block";
        const bar = document.getElementById("progress-fill");
        bar.style.width = "0%";
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) {
                progress = 90;
                clearInterval(interval);
            }
            bar.style.width = `${progress}%`;
        }, 200);
        wrap.dataset.interval = interval;
    } else {
        const bar = document.getElementById("progress-fill");
        bar.style.width = "100%";
        if (wrap.dataset.interval) {
            clearInterval(parseInt(wrap.dataset.interval));
        }
        setTimeout(() => {
            wrap.style.display = "none";
            bar.style.width = "0%";
        }, 400);
    }
}

function hideScrapeResults() {
    document.getElementById("results-section").style.display = "none";
}

function hideConvertResults() {
    document.getElementById("convert-results").style.display = "none";
}
