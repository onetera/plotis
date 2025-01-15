document.querySelectorAll(".openPopup6").forEach(button => {
      button.addEventListener("click", function () {
        const file = this.getAttribute("data-file");
        const targetId = this.getAttribute("data-target");
        const targetContainer = document.getElementById(targetId);

        // 팝업 파일 로드
        fetch(file)
          .then(response => response.text())
          .then(html => {
            targetContainer.innerHTML = html;

            // 스케줄러 초기화
            createSchedule([ // 첫 번째 스케줄러
              { name: "시나리오개발", duration: 6, color: "#ff3b2f" },
              { name: "캐스팅", duration: 4, color: "#ff3b2f" },
              { name: "로케이션 스카우팅", duration: 3, color: "#ff3b2f" },
              { name: "아트 디렉션 및 세트디자인", duration: 4, color: "#ff3b2f" },
              { name: "스토리보드 제작", duration: 3, color: "#ff3b2f" },
              { name: "리허설 및 워크샵", duration: 2, color: "#ff3b2f" }
            ], 22);

            createSchedule2([ // 두 번째 스케줄러
              { name: "촬영", duration: 18, color: "#ff9500" },
              { name: "일일 촬영검토", duration: 18, color: "#ff9500" }
            ], 36);

            createSchedule3([ // 세 번째 스케줄러
              { name: "편집", duration: 8, color: "#35c759" },
              { name: "시각효과 및 색보정", duration: 16, color: "#35c759" },
              { name: "사운드 디자인 및 믹싱", duration: 12, color: "#35c759" },
              { name: "최종 검수 및 수정", duration: 4, color: "#35c759" }
            ], 40);

            createSchedule4([ // 네 번째 스케줄러
              { name: "마케팅 전략 수립", duration: 4, color: "#00c7be" },
              { name: "트레일러 제작", duration: 3, color: "#00c7be" },
              { name: "시사회 및 언론 공개", duration: 2, color: "#00c7be" },
              { name: "개봉 전 프로모션", duration: 3, color: "#00c7be" }
            ], 12);
          });
      });
    });

    function createSchedule(tasks, totalWeeks) {
      renderSchedule(tasks, "schedule", "Preproduction", totalWeeks);
    }

    function createSchedule2(tasks, totalWeeks) {
      renderSchedule(tasks, "schedule", "Production", totalWeeks);
    }

    function createSchedule3(tasks, totalWeeks) {
      renderSchedule(tasks, "schedule", "Postproduction", totalWeeks);
    }
    function createSchedule4(tasks, totalWeeks) {
      renderSchedule(tasks, "schedule", "P&A", totalWeeks);
    }


    function renderSchedule(tasks, containerId, title, totalWeeks) {
      const schedule = document.getElementById(containerId);

      if (!schedule) {
        console.error("스케줄러 컨테이너가 없습니다!");
        return;
      }

      let currentStart = 0;
      let totalDuration = 0;

      // 제목 추가
      const titleElement = document.createElement("div");
      titleElement.textContent = title;
      titleElement.className = "total-duration-tit";
      schedule.appendChild(titleElement);

      tasks.forEach(task => {
        // 작업 줄 생성
        const taskRow = document.createElement("div");
        taskRow.className = "task-row";

        // 작업 이름 생성
        const taskName = document.createElement("div");
        taskName.className = "task-name";
        taskName.textContent = task.name;

        // 작업 바 생성
        const taskElement = document.createElement("div");
        taskElement.className = "task";
        taskElement.style.width = `${(task.duration / totalWeeks) * 100}%`; // 해당 스케줄러의 전체 주 기준
        taskElement.style.marginLeft = `${(currentStart / totalWeeks) * 100}%`;
        taskElement.style.backgroundColor = task.color;

        // 작업 바 위의 텍스트
        const taskText = document.createElement("span");
        taskText.className = "task-text";
        taskText.textContent = `${task.duration} weeks`;
        taskElement.appendChild(taskText);

        // DOM 추가
        taskRow.appendChild(taskName);
        taskRow.appendChild(taskElement);
        schedule.appendChild(taskRow);

        currentStart += task.duration;
        totalDuration += task.duration;
      });

      // 총 주수 추가
      const totalElement = document.createElement("div");
      totalElement.textContent = `총 기간: ${totalDuration} 주`;
      totalElement.className = "total-duration";
      schedule.appendChild(totalElement);
    }
