export const synopData = {
    "1": "시놉시스 1: 서울의 작은 카페에서 시작되는 이야기.",
    "2": "시놉시스 2: 청년 창업자의 도전 이야기.",
    "3": "시놉시스 3: 어려움을 극복하는 성장 이야기.",
    "4": "시놉시스 4: 커피 드림의 성공 비결."
};

export const scenData = {
    "1": "## 시나리오 1\n\n커피 드림 내부에서의 **감동적인 이야기**.",
    "2": "### 시나리오 2\n\n도시의 아침, 새로운 도전.",
    "3": "#### 중요한 발표 전날\n\n긴장감 넘치는 날의 이야기!",
    "4": "**새로운 시도:** 카페 디자인 변경 프로젝트 시작!"
};

export const schedData = {
    "1": {
        schedules: [
            {
                title: "Preproduction",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "시나리오개발", duration: 6, colorIndex: 0 },
                    { name: "캐스팅", duration: 4, colorIndex: 0 },
                    { name: "로케이션 스카우팅", duration: 3, colorIndex: 0 },
                    { name: "아트 디렉션 및 세트디자인", duration: 4, colorIndex: 0 },
                    { name: "스토리보드 제작", duration: 3, colorIndex: 0 },
                    { name: "리허설 및 워크샵", duration: 2, colorIndex: 0 }
                ],
                totalWeeks: 22
            },
            {
                title: "Production",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "촬영", duration: 18, colorIndex: 1 },
                    { name: "일일 촬영검토", duration: 18, colorIndex: 1 }
                ],
                totalWeeks: 36
            },
            {
                title: "Postproduction",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "편집", duration: 8, colorIndex: 2 },
                    { name: "시각효과 및 색보정", duration: 16, colorIndex: 2 },
                    { name: "사운드 디자인 및 믹싱", duration: 12, colorIndex: 2 },
                    { name: "최종 검수 및 수정", duration: 4, colorIndex: 2 }
                ],
                totalWeeks: 40
            },
            {
                title: "P&A",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "마케팅 전략 수립", duration: 4, colorIndex: 3 },
                    { name: "트레일러 제작", duration: 3, colorIndex: 3 },
                    { name: "시사회 및 언론 공개", duration: 2, colorIndex: 3 },
                    { name: "개봉 전 프로모션", duration: 3, colorIndex: 3 }
                ],
                totalWeeks: 12
            }
        ]
    },
    "2": {
        schedules: [
            {
                title: "Production",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "촬영", duration: 18, colorIndex: 0 },
                    { name: "일일 촬영검토", duration: 18, colorIndex: 0 }
                ],
                totalWeeks: 36
            },
            {
                title: "Postproduction",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "편집", duration: 8, colorIndex: 2 },
                    { name: "시각효과 및 색보정", duration: 16, colorIndex: 2 },
                    { name: "사운드 디자인 및 믹싱", duration: 12, colorIndex: 2 },
                    { name: "최종 검수 및 수정", duration: 4, colorIndex: 2 }
                ],
                totalWeeks: 40
            },
            {
                title: "P&A",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "마케팅 전략 수립", duration: 4, colorIndex: 3 },
                    { name: "트레일러 제작", duration: 3, colorIndex: 3 },
                    { name: "시사회 및 언론 공개", duration: 2, colorIndex: 3 },
                    { name: "개봉 전 프로모션", duration: 3, colorIndex: 3 }
                ],
                totalWeeks: 12
            }
        ]
    },
    "3": {
        schedules: [
            {
                title: "P&A",
                colors: ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"],
                tasks: [
                    { name: "마케팅 전략 수립", duration: 4, colorIndex: 3 },
                    { name: "트레일러 제작", duration: 3, colorIndex: 3 },
                    { name: "시사회 및 언론 공개", duration: 2, colorIndex: 3 },
                    { name: "개봉 전 프로모션", duration: 3, colorIndex: 3 }
                ],
                totalWeeks: 12
            }
        ]
    }
};

export const budgetData = {
  "1": {
    headers: ["항목", "기간", "세부항목", "가격"],
    tasks: [
      {
        title: "Preproduction",
        duration: "6주",
        name: "시나리오개발",
        value: 100000000
      },
      {
        title: "Preproduction",
        duration: "4주",
        name: "캐스팅",
        value: 200000000
      },
      {
        title: "Preproduction",
        duration: "3주",
        name: "로케이션 스카우팅",
        value: 150000000
      },
      {
        title: "Preproduction",
        duration: "4주",
        name: "아트 디렉션 및 세트 디자인",
        value: 300000000
      },
      {
        title: "Preproduction",
        duration: "3주",
        name: "스토리보드제작",
        value: 50000000
      },
      {
        title: "Preproduction",
        duration: "2주",
        name: "리허설 및 워크샵",
        value: 100000000
      },
      {
        title: "Production",
        duration: "18주",
        name: "촬영",
        value: 1500000000
      },
      {
        title: "Production",
        duration: "18주",
        name: "일일 촬영 검토",
        value: 200000000
      },
      {
        title: "Postproduction",
        duration: "8주",
        name: "편집",
        value: 300000000
      },
      {
        title: "Postproduction",
        duration: "16주",
        name: "시각 효과 및 색보정",
        value: 500000000
      },
      {
        title: "Postproduction",
        duration: "12주",
        name: "사운드 디자인 및 믹싱",
        value: 200000000
      },
      {
        title: "Postproduction",
        duration: "4주",
        name: "최종 검수 및 수정",
        value: 100000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "4주",
        name: "마케팅 전략 수립",
        value: 150000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "3주",
        name: "트레일러 제작",
        value: 100000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "2주",
        name: "시사회 및 언론 공개",
        value: 80000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "3주",
        name: "개봉 전 프로모션",
        value: 80000000
      }
    ],
    "footer": {
      totalLabel: "Total",
      totalPrice: 0,  // 초기 총합은 0으로 설정
    }
  },
  "2": {
    headers: ["항목", "기간", "세부항목", "가격"],
    tasks: [
      {
        title: "Preproduction",
        duration: "6주",
        name: "시나리오개발",
        value: 150000000
      },
      {
        title: "Preproduction",
        duration: "4주",
        name: "캐스팅",
        value: 230000000
      },
      {
        title: "Preproduction",
        duration: "3주",
        name: "로케이션 스카우팅",
        value: 150000000
      },
      {
        title: "Preproduction",
        duration: "4주",
        name: "아트 디렉션 및 세트 디자인",
        value: 300000000
      },
      {
        title: "Preproduction",
        duration: "3주",
        name: "스토리보드제작",
        value: 50000000
      },
      {
        title: "Preproduction",
        duration: "2주",
        name: "리허설 및 워크샵",
        value: 100000000
      },
      {
        title: "Production",
        duration: "18주",
        name: "촬영",
        value: 1500000000
      },
      {
        title: "Production",
        duration: "18주",
        name: "일일 촬영 검토",
        value: 200000000
      },
      {
        title: "Postproduction",
        duration: "8주",
        name: "편집",
        value: 300000000
      },
      {
        title: "Postproduction",
        duration: "16주",
        name: "시각 효과 및 색보정",
        value: 500000000
      },
      {
        title: "Postproduction",
        duration: "12주",
        name: "사운드 디자인 및 믹싱",
        value: 200000000
      },
      {
        title: "Postproduction",
        duration: "4주",
        name: "최종 검수 및 수정",
        value: 100000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "4주",
        name: "마케팅 전략 수립",
        value: 150000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "3주",
        name: "트레일러 제작",
        value: 100000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "2주",
        name: "시사회 및 언론 공개",
        value: 80000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "3주",
        name: "개봉 전 프로모션",
        value: 80000000
      }
    ],
    "footer": {
      totalLabel: "Total",
      totalPrice: 0,  // 초기 총합은 0으로 설정
    }
  },
  "3": {
    headers: ["항목", "기간", "세부항목", "가격"],
    tasks: [
      {
        title: "Preproduction",
        duration: "6주",
        name: "시나리오개발",
        value: 10000000
      },
      {
        title: "Preproduction",
        duration: "4주",
        name: "캐스팅",
        value: 200000000
      },
      {
        title: "Preproduction",
        duration: "3주",
        name: "로케이션 스카우팅",
        value: 150000000
      },
      {
        title: "Preproduction",
        duration: "4주",
        name: "아트 디렉션 및 세트 디자인",
        value: 300000000
      },
      {
        title: "Preproduction",
        duration: "3주",
        name: "스토리보드제작",
        value: 50000000
      },
      {
        title: "Preproduction",
        duration: "2주",
        name: "리허설 및 워크샵",
        value: 100000000
      },
      {
        title: "Production",
        duration: "18주",
        name: "촬영",
        value: 1500000000
      },
      {
        title: "Production",
        duration: "18주",
        name: "일일 촬영 검토",
        value: 200000000
      },
      {
        title: "Postproduction",
        duration: "8주",
        name: "편집",
        value: 300000000
      },
      {
        title: "Postproduction",
        duration: "16주",
        name: "시각 효과 및 색보정",
        value: 500000000
      },
      {
        title: "Postproduction",
        duration: "12주",
        name: "사운드 디자인 및 믹싱",
        value: 200000000
      },
      {
        title: "Postproduction",
        duration: "4주",
        name: "최종 검수 및 수정",
        value: 100000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "4주",
        name: "마케팅 전략 수립",
        value: 150000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "3주",
        name: "트레일러 제작",
        value: 100000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "2주",
        name: "시사회 및 언론 공개",
        value: 80000000
      },
      {
        title: "P&A (Publicity & Advertising)",
        duration: "3주",
        name: "개봉 전 프로모션",
        value: 80000000
      }
    ],
    "footer": {
      totalLabel: "Total",
      totalPrice: 0,  // 초기 총합은 0으로 설정
    }
  }
};
