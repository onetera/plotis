window.onload = function() {
    const content = document.getElementById('contents');

    // 로딩 컨테이너를 위한 div 생성
    const loadingContainer = document.createElement('div');
    loadingContainer.classList.add('loading-container'); // 로딩 컨테이너 클래스 추가

    // 로딩 애니메이션을 위한 div 생성
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('loading');

    // "LOADING" 애니메이션을 위한 h2 생성
    const aliensH1 = document.createElement('h2');
    aliensH1.className = 'aliens'; // 클래스 추가
    const aliensText = 'LOADING';
    for (let char of aliensText) {
        const div = document.createElement('div');
        div.textContent = char; // 각 문자 추가
        aliensH1.appendChild(div);
    }

    // 로딩 div에 ALIENS 텍스트 추가
    loadingDiv.appendChild(aliensH1);

    // 프로세스 바와 숫자
    const processContainer = document.createElement('div');
    processContainer.classList.add('process-container');

    // 프로세스 바 내부 색상 채워지는 부분
    const processBar = document.createElement('div');
    processBar.classList.add('process-bar');
    processContainer.appendChild(processBar);

    // 로딩 텍스트 (숫자 표시 부분)
    const loadingText = document.createElement('div');
    loadingText.classList.add('loading-text');
    loadingText.innerText = '0%'; // 초기 텍스트 설정
    processContainer.appendChild(loadingText);

    loadingDiv.appendChild(processContainer); // 로딩 div에 프로세스 바 추가

    // 생성한 로딩 컨테이너를 content에 추가
    loadingContainer.appendChild(loadingDiv);
    content.appendChild(loadingContainer);

    // 진행률 애니메이션
    let process = 0;
    const interval = setInterval(function() {
        process += 1;
        processBar.style.width = process + '%'; // 프로세스 바 채워지기
        loadingText.innerText = `${process}%`; // 숫자 올라가기

        // 배경 색상 변경 (예: 파란색에서 초록색으로)
        const colorprocess = Math.floor(process * 2.55); // 0~255로 색상 변화
        processBar.style.backgroundColor = `${255 - colorprocess}, 100)`; // 색상 변화

        if (process === 100) {
            clearInterval(interval); // 100%에 도달하면 진행을 멈춤
            setTimeout(function() {
                // 로딩 애니메이션 숨기고 동영상과 메시지를 표시
                loadingDiv.style.display = 'none';

              // "로딩 완료" 메시지와 동영상 표시
              const loadedDiv = document.createElement('div');
              loadedDiv.classList.add('loaded');
              loadedDiv.innerText = 'PLOTIS';


                // 로딩 애니메이션을 숨기고 동영상 팝업을 표시
              const popupOverlay = document.createElement('div');
              popupOverlay.classList.add('pop-overlay');

              // 팝업 내용 (동영상 포함)
              const popupContent = document.createElement('div');
              popupContent.classList.add('pop-content');

              // 팝업 닫기 버튼 추가
              const closeButton = document.createElement('button');
              closeButton.classList.add('close-btn');
              closeButton.innerHTML = '×'; // '×' 버튼
              closeButton.onclick = function() {
                  popupOverlay.style.opacity = 0; // 팝업을 서서히 숨김
                  setTimeout(function() {
                      popupOverlay.style.display = 'none'; // 완전히 숨김
                  }, 1000); // 1초 후 완전히 숨김
              };

              popupContent.appendChild(closeButton);

                // 동영상 추가
                const video = document.createElement('video');
                video.setAttribute('autoplay', true); // 자동 재생 속성 추가
                video.setAttribute('muted', true); // 브라우저 정책으로 자동 재생을 위해 음소거 필요
                video.setAttribute('controls', true); // 사용자 컨트롤 표시
                const videoSource = document.createElement('source');
                videoSource.setAttribute('src', '/static/media/media.mp4');
                // videoSource.setAttribute('src', './media/media.mp4');
                videoSource.setAttribute('type', 'video/mp4');

                video.appendChild(videoSource);
                popupContent.appendChild(video);

                // 팝업 내용 div에 동영상 추가
                popupOverlay.appendChild(popupContent);

                // 팝업 표시
                document.body.appendChild(popupOverlay);

                // 팝업 서서히 보이게 만들기
                setTimeout(function() {
                    popupOverlay.style.display = 'flex'; // flex로 display: block으로 변경
                    popupOverlay.style.opacity = 1; // 1초 동안 서서히 나타나게 설정
                    content.appendChild(loadedDiv);
                }, 100); // 100ms 후 팝업 보이기 시작

                // 동영상 서서히 열리게 하기 위한 효과 추가


            }, 500); // 500ms 후 동영상 표시
        }
    }, 30); // 30ms마다 진행률 1%씩 증가
};
