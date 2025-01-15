  window.onload = () => {
      // 현재 페이지 제목 가져오기
      const currentPageTitle = document.title.trim().toLowerCase();

      // 모든 <label> 요소 찾기
      const labels = document.querySelectorAll("#sidebarMenu label");

      // 제목과 이미지의 title 비교 후 스타일 적용
      labels.forEach(label => {
          const icon = label.querySelector("li.icon_up");
          if (!icon) return;

          const img = icon.querySelector("img.svg-icon");
          const span = icon.querySelector("span");
          if (!img || !span) return;

          const imgTitle = img.getAttribute("title").trim().toLowerCase();

          if (imgTitle === currentPageTitle) {
              // 배경색과 텍스트 색상 적용
              icon.style.backgroundColor = "#7998ca";  // 원하는 배경색
              icon.style.color = "white";              // 텍스트 색상

              // 이미지 필터 효과 적용
              img.style.filter = "invert(100%) sepia(0%) saturate(0%) hue-rotate(306deg) brightness(103%) contrast(101%)";

              // <span> 색상 변경
              span.style.color = "white";
          }
      });
  };
