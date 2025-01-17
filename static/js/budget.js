document.addEventListener("DOMContentLoaded", () => {
  document.body.addEventListener("click", (event) => {
    if (event.target.id === "startTyping") {
      const selectedValue = document.querySelector('input[name="contentOptionb"]:checked');  // 선택된 라디오 버튼
      const selectedContent = JSON.parse(selectedValue.getAttribute("data-budget"));  // 해당 콘텐츠의 예산 데이터 가져오기
      const targetContainer = document.getElementById("typingContainerb");

      // const title = selectedContent.title[0];
      // 테이블 생성
      targetContainer.style.display = "block";
      let tableHTML = `
        <div class="budget-box">
          <table class="budgetTable">
            <thead>
              <tr>
                <th>항목</th>
                <th>기간</th>
                <th>세부항목</th>
                <th>가격</th>
              </tr>
            </thead>
            <tbody>
      `;

      // 항목 배열을 반복하여 테이블 행 생성
      selectedContent.tasks.forEach(item => {
        tableHTML += `
          <tr>
            <td>${item.title}</td>
            <td>${item.duration}</td> <!-- 기간 -->
            <td>${item.name}</td> <!-- 세부항목은 name 값으로 대체 -->
            <td>${parseInt(item.value).toLocaleString()}원</td> <!-- 가격 -->
          </tr>
        `;
      });

      // 총합 계산
      const totalPrice = selectedContent.tasks.reduce((sum, item) => sum + parseInt(item.value), 0);

      tableHTML += `
            </tbody>
            <tfoot>
              <tr>
                <th colspan="3">Total</th>
                <th>${totalPrice.toLocaleString()}원</th>
              </tr>
            </tfoot>
          </table>
        </div>
      `;

      targetContainer.innerHTML = tableHTML;
    }
  });
});
