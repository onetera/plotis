document.addEventListener("DOMContentLoaded", () => {

    // **"Load Synop" 버튼 클릭 이벤트**
    document.body.addEventListener("click", (event) => {
        if (event.target.id === "startTyping") {
            const selectedValue = document.querySelector('input[name="contentOption"]:checked');  // 선택된 라디오 버튼 가져오기

            const synopIdx = selectedValue.value;  // 선택된 콘텐츠 ID
            const selectedContent = selectedValue.getAttribute("data-synopsis");  // 데이터 가져오기
            const typingContainer = document.getElementById("typingContainer");

            if (selectedContent) {
                typingContainer.style.display = "block";  // 콘텐츠 표시
                typingContainer.innerHTML = `
                    <div class="popup-content">
                        <h2>Synopsis</h2>
                        <p>${selectedContent}</p>
                    </div>
                `;

                // ajax 추가
                fetch('/load_synop_ajax', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ synop_idx: synopIdx })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                    console.log('session update done, synop_idx =', synopIdx);
                    }
                })
                .catch(err => console.error(err));
            } else {
                alert("해당 콘텐츠가 없습니다.");
            }
        }
    });
});
