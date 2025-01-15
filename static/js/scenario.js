document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", (event) => {
        if (event.target.id === "startTyping") {
            // 해당 버튼에 연결된 컨테이너 ID 가져오기
            const targetContainerId = event.target.getAttribute("data-target");  // 버튼에 설정된 컨테이너 ID

            // 컨테이너 ID에 따른 옵션 이름 매핑
            const containerMappings = {
                typingContainer: 'contentOption',
                typingContainerz: 'contentOptionz',
                typingContainerc: 'contentOptionc',
                typingContainerp: 'contentOptionp',
                typingContainerv: 'contentOptionv',
                typingContainerdu: 'contentOptiondu',
                typingContainerb: 'contentOptionb',
                typingContainerpt: 'contentOptionpt'
            };

            const optionName = containerMappings[targetContainerId];  // 해당 컨테이너에 대응하는 라디오 버튼 그룹 이름

            // 선택된 라디오 버튼 가져오기
            const selectedValue = document.querySelector(`input[name="${optionName}"]:checked`);


            const contentId = selectedValue.value;  // 선택된 콘텐츠 ID
            let selectedContent;


            // 데이터 선택
            let contentTitle;
            // let data, contentTitle;
            if (optionName === 'contentOption') {
                // data = synopData;  // 시놉시스 데이터 사용
                selectedContent = selectedValue.getAttribute("data-synopsis");
                contentTitle = "Synopsis";
            } else if (optionName === 'contentOptionz') {
                // data = scenData;  // 시나리오 데이터 사용
                selectedContent = selectedValue.getAttribute("data-scenario");
                contentTitle = "Scenario";
            }

            // 출력할 컨테이너 가져오기
            const typingContainer = document.getElementById(targetContainerId);

            if (selectedContent) {
                dashscenpbox.style.display = 'block';
                typingContainer.style.display = "block";  // 콘텐츠 표시
                typingContainer.innerHTML = `
                    <div class="popup-content">
                        <h2>${contentTitle.toUpperCase()}</h2>
                        <p>${selectedContent}</p>
                    </div>
                `;

                // ajax 추가
                if (contentTitle === "Synopsis") {
                    fetch("/load_synop_ajax", {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ synop_idx: contentId })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Synopsis session update done, synop_idx =', contentId);
                        }
                    })
                    .catch(err => console.error(err));
                } else if (contentTitle === "Scenario") {
                    fetch("/load_scen_ajax", {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ scen_idx: contentId })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Scenario session update done, scen_idx =', contentId);
                        }
                    })
                    .catch(err => console.error(err));
                }
            } else {
                alert("해당 콘텐츠가 없습니다.");
            }
        }
    });
});
