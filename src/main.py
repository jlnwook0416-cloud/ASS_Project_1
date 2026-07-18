import pygame


# 게임 창의 크기를 정합니다.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# 화면에 사용할 색상을 RGB 값으로 정합니다.
# RGB는 빨강(Red), 초록(Green), 파랑(Blue)의 양을 뜻합니다.
GREEN_BACKGROUND = (34, 139, 34)
GRAY_ROAD = (110, 110, 110)
YELLOW_CENTER_LINE = (255, 215, 0)
RED_CAR_BODY = (220, 45, 45)
DARK_RED_CAR_DETAIL = (150, 20, 20)
SKY_BLUE_WINDOW = (135, 206, 235)
BLACK_TIRE = (15, 15, 15)

# 도로 폭은 화면 너비의 약 40%가 되도록 계산합니다.
ROAD_WIDTH = int(SCREEN_WIDTH * 0.4)

# 도로가 화면 중앙에 오도록 왼쪽 시작 위치를 계산합니다.
ROAD_LEFT_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2

# 도로 중앙에 그릴 노란색 중앙선의 두께입니다.
CENTER_LINE_WIDTH = 6

# 자동차의 크기를 정합니다.
CAR_WIDTH = 60
CAR_HEIGHT = 110

# 자동차가 화면 아래쪽에 오되, 화면 끝과 조금 떨어지도록 여백을 정합니다.
CAR_BOTTOM_MARGIN = 45

# 자동차가 도로 중앙에 오도록 왼쪽 위 위치를 계산합니다.
CAR_X = (SCREEN_WIDTH - CAR_WIDTH) // 2
CAR_Y = SCREEN_HEIGHT - CAR_HEIGHT - CAR_BOTTOM_MARGIN

# 자동차를 구성하는 부품들의 크기입니다.
CAR_BORDER_WIDTH = 4
CAR_WINDOW_WIDTH = 34
CAR_WINDOW_HEIGHT = 24
CAR_TIRE_WIDTH = 12
CAR_TIRE_HEIGHT = 26


def draw_road(screen):
    """화면 중앙에 세로 도로와 노란색 중앙선을 그립니다."""

    # 도로는 화면 위쪽부터 아래쪽까지 이어지는 회색 사각형입니다.
    road_rectangle = pygame.Rect(
        ROAD_LEFT_X,
        0,
        ROAD_WIDTH,
        SCREEN_HEIGHT,
    )
    pygame.draw.rect(screen, GRAY_ROAD, road_rectangle)

    # 도로의 정확한 중앙 위치를 계산합니다.
    # 이 위치에 노란색 선 1개만 그려서 도로 중앙선을 표현합니다.
    center_line_x = ROAD_LEFT_X + (ROAD_WIDTH // 2)

    pygame.draw.line(
        screen,
        YELLOW_CENTER_LINE,
        (center_line_x, 0),
        (center_line_x, SCREEN_HEIGHT),
        CENTER_LINE_WIDTH,
    )


def draw_car(screen):
    """도로 중앙 아래쪽에 위에서 내려다본 빨간색 자동차를 그립니다."""

    # 자동차 전체 차체를 빨간색 세로 사각형으로 그립니다.
    car_body = pygame.Rect(CAR_X, CAR_Y, CAR_WIDTH, CAR_HEIGHT)
    pygame.draw.rect(screen, RED_CAR_BODY, car_body)

    # 자동차 가장자리에 어두운 빨간색 테두리를 그려 입체감을 줍니다.
    pygame.draw.rect(screen, DARK_RED_CAR_DETAIL, car_body, CAR_BORDER_WIDTH)

    # 앞유리는 자동차 위쪽에 있는 하늘색 사각형입니다.
    front_window = pygame.Rect(
        CAR_X + (CAR_WIDTH - CAR_WINDOW_WIDTH) // 2,
        CAR_Y + 18,
        CAR_WINDOW_WIDTH,
        CAR_WINDOW_HEIGHT,
    )
    pygame.draw.rect(screen, SKY_BLUE_WINDOW, front_window)

    # 뒷유리는 자동차 아래쪽에 있는 하늘색 사각형입니다.
    rear_window = pygame.Rect(
        CAR_X + (CAR_WIDTH - CAR_WINDOW_WIDTH) // 2,
        CAR_Y + CAR_HEIGHT - CAR_WINDOW_HEIGHT - 18,
        CAR_WINDOW_WIDTH,
        CAR_WINDOW_HEIGHT,
    )
    pygame.draw.rect(screen, SKY_BLUE_WINDOW, rear_window)

    # 차체 가운데에 어두운 빨간색 장식선을 그려 자동차 모양을 더 잘 보이게 합니다.
    pygame.draw.line(
        screen,
        DARK_RED_CAR_DETAIL,
        (CAR_X + CAR_WIDTH // 2, CAR_Y + 48),
        (CAR_X + CAR_WIDTH // 2, CAR_Y + CAR_HEIGHT - 48),
        3,
    )

    # 왼쪽 앞바퀴를 검은색 사각형으로 그립니다.
    front_left_tire = pygame.Rect(
        CAR_X - CAR_TIRE_WIDTH,
        CAR_Y + 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, front_left_tire)

    # 오른쪽 앞바퀴를 검은색 사각형으로 그립니다.
    front_right_tire = pygame.Rect(
        CAR_X + CAR_WIDTH,
        CAR_Y + 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, front_right_tire)

    # 왼쪽 뒷바퀴를 검은색 사각형으로 그립니다.
    rear_left_tire = pygame.Rect(
        CAR_X - CAR_TIRE_WIDTH,
        CAR_Y + CAR_HEIGHT - CAR_TIRE_HEIGHT - 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, rear_left_tire)

    # 오른쪽 뒷바퀴를 검은색 사각형으로 그립니다.
    rear_right_tire = pygame.Rect(
        CAR_X + CAR_WIDTH,
        CAR_Y + CAR_HEIGHT - CAR_TIRE_HEIGHT - 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, rear_right_tire)


def main():
    """pygame을 시작하고 창이 닫힐 때까지 프로그램을 실행합니다."""

    # pygame 기능을 사용하기 전에 반드시 초기화합니다.
    pygame.init()

    # 1000x700 크기의 창을 만들고 제목을 설정합니다.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ASS V1.0 - Road")

    # 게임 루프가 계속 실행될지 저장하는 변수입니다.
    is_running = True

    # 창을 닫거나 ESC 키를 누를 때까지 반복합니다.
    while is_running:
        # 사용자가 발생시킨 이벤트를 하나씩 확인합니다.
        for event in pygame.event.get():
            # 창 닫기 버튼을 누르면 반복을 끝냅니다.
            if event.type == pygame.QUIT:
                is_running = False

            # 키보드를 눌렀고, 그 키가 ESC라면 반복을 끝냅니다.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_running = False

        # 먼저 전체 화면을 초록색 배경으로 채웁니다.
        screen.fill(GREEN_BACKGROUND)

        # 배경 위에 도로와 노란색 중앙선을 그립니다.
        draw_road(screen)

        # 도로 위에 움직이지 않는 빨간색 자동차를 그립니다.
        draw_car(screen)

        # 지금까지 그린 내용을 실제 창에 보여줍니다.
        pygame.display.flip()

    # pygame을 종료하여 사용한 자원을 정리합니다.
    pygame.quit()


# 이 파일을 직접 실행했을 때만 main 함수를 실행합니다.
if __name__ == "__main__":
    main()
