document.addEventListener("DOMContentLoaded", () => {
  document.body.addEventListener("click", (event) => {
    if (event.target.id === "startTyping") {
      const selectedValue = document.querySelector('input[name="contentOptiondu"]:checked');  // 선택된 라디오 버튼
      const selectedContent = JSON.parse(selectedValue.getAttribute("data-schedule"));  // 해당 콘텐츠의 예산 데이터 가져오기
      const targetContainer = document.getElementById("typingContainerdu");

      // 콘텐츠를 표시할 스케줄러 컨테이너 구조 삽입
      targetContainer.style.display = "block";
      targetContainer.innerHTML = `
        <div class="progress_box">
          <div id="schedule" class="schedule-container"></div>
        </div>
      `;

      const scheduleContainer = document.getElementById("schedule");

      // 스케줄 데이터를 렌더링
      selectedContent.schedules.forEach(schedule => {
        renderSchedule(
          schedule.tasks,
          "schedule",
          schedule.title,
          schedule.totalWeeks,
          schedule.colors
        );
      });
    }
  });

  function renderSchedule(tasks, containerId, title, totalWeeks, colors) {
    const schedule = document.getElementById(containerId);

    if (!schedule) {
      console.error("스케줄러 컨테이너가 없습니다!");
      return;
    }

    // 기존 내용 초기화
    schedule.innerHTML += `<div class="total-duration-tit">${title}</div>`;

    let currentStart = 0;
    let totalDuration = 0;

    tasks.forEach(task => {
      const taskRow = document.createElement("div");
      taskRow.className = "task-row";

      const taskName = document.createElement("div");
      taskName.className = "task-name";
      taskName.textContent = task.name;

      const taskElement = document.createElement("div");
      taskElement.className = "task";
      taskElement.style.width = `${(task.duration / totalWeeks) * 100}%`;
      taskElement.style.marginLeft = `${(currentStart / totalWeeks) * 100}%`;

        // colorIndex로 색상 참조
      const taskColor = colors[task.colorIndex];
      taskElement.style.backgroundColor = taskColor;

      const taskText = document.createElement("span");
      taskText.className = "task-text";
      taskText.textContent = `${task.duration} weeks`;
      taskElement.appendChild(taskText);

      taskRow.appendChild(taskName);
      taskRow.appendChild(taskElement);
      schedule.appendChild(taskRow);

      currentStart += task.duration;
      totalDuration += task.duration;
    });

    const totalElement = document.createElement("div");
    totalElement.textContent = `총 기간: ${totalDuration} 주`;
    totalElement.className = "total-duration";
    schedule.appendChild(totalElement);
  }
});
