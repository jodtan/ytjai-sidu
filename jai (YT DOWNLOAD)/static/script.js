document.getElementById('downloadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const url = document.getElementById('youtubeUrl').value.trim();
    if (!url) {
        alert('Please enter a valid YouTube URL');
        return;
    }

    const response = await fetch('/fetch_info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });

    const data = await response.json();
    if (data.error) {
        alert(`Error: ${data.error}`);
        return;
    }

    document.getElementById('contentSection').classList.remove('hidden');
    document.getElementById('videoThumbnail').src = data.thumbnail;
    document.getElementById('videoTitle').textContent = data.title;

    const formatSelect = document.getElementById('formatQuality');
    formatSelect.innerHTML = '';
    data.formats.forEach((format) => {
        const option = document.createElement('option');
        option.value = format.format_id;
        option.textContent = format.format;
        formatSelect.appendChild(option);
    });
});

document.getElementById('downloadButton').addEventListener('click', async function () {
    const url = document.getElementById('youtubeUrl').value.trim();
    const format_id = document.getElementById('formatQuality').value;

    const response = await fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, format_id }),
    });

    if (response.ok) {
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'download';
        link.click();
    } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
    }
});
