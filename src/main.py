import pygame


# 게임 창의 크기를 정합니다.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# 화면에 사용할 색상을 RGB 값으로 정합니다.
# RGB는 빨강(Red), 초록(Green), 파랑(Blue)의 양을 뜻합니다.
GREEN_BACKGROUND = (34, 139, 34)
GRAY_ROAD = (110, 110, 110)
YELLOW_CENTER_LINE = (255, 215, 0)
WHITE_ROAD_EDGE = (245, 245, 245)
RED_CAR_BODY = (220, 45, 45)
DARK_RED_CAR_DETAIL = (150, 20, 20)
BLUE_CAR_BODY = (45, 95, 230)
DARK_BLUE_CAR_DETAIL = (20, 45, 150)
SKY_BLUE_WINDOW = (135, 206, 235)
BLACK_TIRE = (15, 15, 15)
WHITE_TEXT = (255, 255, 255)
SENSOR_LINE_COLOR = (255, 245, 120)

# 왕복 6차선 도로를 만들기 위한 차선 개수입니다.
TOTAL_LANE_COUNT = 6
ONE_WAY_LANE_COUNT = TOTAL_LANE_COUNT // 2

# 차선 폭은 화면 너비를 기준으로 정하고, 도로 폭은 차선 6개를 합쳐 계산합니다.
LANE_WIDTH = int(SCREEN_WIDTH * 0.12)
ROAD_WIDTH = LANE_WIDTH * TOTAL_LANE_COUNT

# 도로가 화면 중앙에 오도록 왼쪽/오른쪽 경계 위치를 계산합니다.
LEFT_ROAD_EDGE_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2
RIGHT_ROAD_EDGE_X = LEFT_ROAD_EDGE_X + ROAD_WIDTH

# 도로 중앙에 그릴 노란색 중앙선의 두께입니다.
CENTER_LINE_WIDTH = 6

# 도로 양쪽 가장자리에 그릴 흰색 실선의 두께입니다.
ROAD_EDGE_LINE_WIDTH = 5

# 같은 방향 안의 차선을 나누는 흰색 점선의 두께입니다.
LANE_SEPARATOR_LINE_WIDTH = 4

# 차선 한 조각의 길이와 차선 사이의 빈 공간입니다.
LANE_DASH_LENGTH = 70
LANE_DASH_GAP = 45

# 게임 화면이 너무 빠르게 반복되지 않도록 초당 프레임 수를 정합니다.
FPS = 60

# 자동차의 크기를 차선 폭에 맞춰 정합니다.
CAR_WIDTH = int(LANE_WIDTH * 0.5)
CAR_HEIGHT = int(CAR_WIDTH * 1.8)

# 자동차가 화면 아래쪽에 오되, 화면 끝과 조금 떨어지도록 여백을 정합니다.
CAR_BOTTOM_MARGIN = 45

# 자동차 이동 속도입니다. 숫자가 클수록 자동차가 더 빠르게 움직입니다.
CAR_SPEED = 5

# 도로 스크롤 속도입니다. 자동차가 기준 위치에 도달한 뒤 차선이 내려가는 속도입니다.
ROAD_SCROLL_SPEED = 5

# 자동차의 화면 기준 위치입니다. 이 위치에 도달하면 자동차 대신 차선이 움직입니다.
CAR_CAMERA_LIMIT_Y = int(SCREEN_HEIGHT * 0.7)

# 각 차선의 가운데 X좌표를 계산합니다. 장애물 배치나 차선 유지 기능에서 다시 사용할 수 있습니다.
LANE_CENTER_X_LIST = tuple(
    LEFT_ROAD_EDGE_X + (lane_index * LANE_WIDTH) + (LANE_WIDTH // 2)
    for lane_index in range(TOTAL_LANE_COUNT)
)

# 노란색 중앙 분리선은 왼쪽 3개 차선과 오른쪽 3개 차선 사이에 있습니다.
CENTER_DIVIDER_LINE_X = LEFT_ROAD_EDGE_X + (LANE_WIDTH * ONE_WAY_LANE_COUNT)

# 자동차가 처음 시작할 위치입니다.
# 오른쪽 방향 3개 차선 중 가운데 차선의 중심에 자동차를 배치합니다.
RIGHT_DIRECTION_MIDDLE_LANE_INDEX = ONE_WAY_LANE_COUNT + (ONE_WAY_LANE_COUNT // 2)
START_CAR_CENTER_X = LANE_CENTER_X_LIST[RIGHT_DIRECTION_MIDDLE_LANE_INDEX]
START_CAR_X = START_CAR_CENTER_X - (CAR_WIDTH // 2)
START_CAR_Y = SCREEN_HEIGHT - CAR_HEIGHT - CAR_BOTTOM_MARGIN

# 장애물 자동차는 플레이어 자동차보다 앞쪽에 배치합니다.
# 같은 차선의 중앙 X좌표를 사용하면 차선 중앙에 정확히 놓을 수 있습니다.
OBSTACLE_CAR_LANE_INDEX = RIGHT_DIRECTION_MIDDLE_LANE_INDEX
OBSTACLE_CAR_DISTANCE_AHEAD = 500
OBSTACLE_CAR_WORLD_Y = START_CAR_Y - OBSTACLE_CAR_DISTANCE_AHEAD

# 자동차를 구성하는 부품들의 크기입니다.
CAR_BORDER_WIDTH = 4
CAR_WINDOW_WIDTH = 34
CAR_WINDOW_HEIGHT = 24
CAR_TIRE_WIDTH = 12
CAR_TIRE_HEIGHT = 26

# 거리 표시 글자의 크기입니다.
DISTANCE_TEXT_SIZE = 28

# 자동차가 장애물에 이 거리 이하로 가까워지면 전진을 막습니다.
STOP_DISTANCE = 80


def draw_dashed_vertical_line(screen, color, line_x, road_scroll_y, line_width):
    """카메라 스크롤에 맞춰 세로 점선을 자연스럽게 이어 그립니다."""

    # 스크롤 값만큼 점선 시작 위치를 아래로 밀어 자동차가 전진하는 느낌을 냅니다.
    lane_cycle = LANE_DASH_LENGTH + LANE_DASH_GAP
    lane_start_y = (road_scroll_y % lane_cycle) - lane_cycle

    while lane_start_y < SCREEN_HEIGHT:
        lane_end_y = lane_start_y + LANE_DASH_LENGTH

        pygame.draw.line(
            screen,
            color,
            (line_x, lane_start_y),
            (line_x, lane_end_y),
            line_width,
        )

        lane_start_y += lane_cycle


def limit_car_position(car_x, car_y):
    """자동차가 화면 밖으로 나가지 않도록 좌표를 제한합니다."""

    # 좌우 도로 경계 제한: 바퀴까지 포함한 자동차의 왼쪽/오른쪽 끝을 도로 안에 둡니다.
    min_car_x = LEFT_ROAD_EDGE_X + CAR_TIRE_WIDTH
    max_car_x = LEFT_ROAD_EDGE_X + ROAD_WIDTH - CAR_WIDTH - CAR_TIRE_WIDTH

    # 화면 밖 이동 제한: 자동차의 위쪽/아래쪽 끝을 화면 안에 둡니다.
    min_car_y = 0
    max_car_y = SCREEN_HEIGHT - CAR_HEIGHT

    car_x = max(min_car_x, min(car_x, max_car_x))
    car_y = max(min_car_y, min(car_y, max_car_y))

    return car_x, car_y


def calculate_front_distance(player_x, player_y, road_scroll_y, obstacle_car):
    """플레이어 자동차 앞쪽과 장애물 자동차 뒤쪽 사이의 빈 공간을 계산합니다."""

    # 화면에서 보이는 player_y를 월드 좌표로 바꿉니다.
    # 도로가 스크롤되어도 월드 좌표로 계산하면 실제 거리가 흔들리지 않습니다.
    player_world_y = player_y - road_scroll_y

    player_left_x = player_x
    player_right_x = player_x + CAR_WIDTH
    obstacle_left_x = obstacle_car.x
    obstacle_right_x = obstacle_car.x + CAR_WIDTH

    # X축 영역이 겹칠 때만 앞쪽 센서에 잡힌 것으로 봅니다.
    # 옆 차선으로 이동해서 겹치지 않으면 감지하지 않습니다.
    is_x_overlapping = (
        player_left_x < obstacle_right_x
        and player_right_x > obstacle_left_x
    )
    if not is_x_overlapping:
        return None

    # 자동차는 위쪽이 앞부분입니다. 장애물의 뒷부분은 world_y + CAR_HEIGHT입니다.
    player_front_world_y = player_world_y
    obstacle_rear_world_y = obstacle_car.world_y + CAR_HEIGHT

    # 장애물이 플레이어보다 앞에 있고, 두 자동차 사이에 빈 공간이 있을 때만 거리를 반환합니다.
    empty_space_distance = player_front_world_y - obstacle_rear_world_y
    if empty_space_distance < 0:
        return None

    return int(empty_space_distance)


def draw_distance_text(screen, font, front_distance):
    """거리 감지 결과를 화면 왼쪽 위에 표시합니다."""

    if front_distance is None:
        distance_text = "Distance: No obstacle"
    elif front_distance <= STOP_DISTANCE:
        distance_text = f"Distance: {front_distance} px - STOP"
    else:
        distance_text = f"Distance: {front_distance} px"

    text_image = font.render(distance_text, True, WHITE_TEXT)
    screen.blit(text_image, (20, 20))


def draw_front_sensor_line(screen, player_x, player_y, obstacle_car, road_scroll_y):
    """감지 중일 때 플레이어 앞쪽 중앙에서 장애물 뒤쪽 중앙까지 센서 선을 그립니다."""

    # 선은 실제 화면에 그려야 하므로 화면 좌표를 사용합니다.
    player_front_center = (
        player_x + (CAR_WIDTH // 2),
        player_y,
    )
    obstacle_rear_center = (
        obstacle_car.x + (CAR_WIDTH // 2),
        obstacle_car.get_screen_y(road_scroll_y) + CAR_HEIGHT,
    )

    pygame.draw.line(
        screen,
        SENSOR_LINE_COLOR,
        player_front_center,
        obstacle_rear_center,
        2,
    )


def is_obstacle_too_close(front_distance):
    """앞쪽 장애물이 정지 기준 거리 안에 있는지 확인합니다."""

    return front_distance is not None and front_distance <= STOP_DISTANCE


def draw_road(screen, road_scroll_y):
    """화면 중앙에 세로 도로와 노란색 중앙선을 그립니다."""

    # 도로는 화면 위쪽부터 아래쪽까지 이어지는 회색 사각형입니다.
    road_rectangle = pygame.Rect(
        LEFT_ROAD_EDGE_X,
        0,
        ROAD_WIDTH,
        SCREEN_HEIGHT,
    )
    pygame.draw.rect(screen, GRAY_ROAD, road_rectangle)

    # 도로의 왼쪽과 오른쪽 가장자리에 끊기지 않는 흰색 실선을 그립니다.
    pygame.draw.line(
        screen,
        WHITE_ROAD_EDGE,
        (LEFT_ROAD_EDGE_X, 0),
        (LEFT_ROAD_EDGE_X, SCREEN_HEIGHT),
        ROAD_EDGE_LINE_WIDTH,
    )
    pygame.draw.line(
        screen,
        WHITE_ROAD_EDGE,
        (RIGHT_ROAD_EDGE_X, 0),
        (RIGHT_ROAD_EDGE_X, SCREEN_HEIGHT),
        ROAD_EDGE_LINE_WIDTH,
    )

    # 차선 사이의 점선 위치를 반복문으로 계산합니다.
    for separator_index in range(1, TOTAL_LANE_COUNT):
        separator_line_x = LEFT_ROAD_EDGE_X + (LANE_WIDTH * separator_index)

        # 가운데 분리선은 노란색, 같은 방향 안의 차선 구분선은 흰색으로 그립니다.
        if separator_line_x == CENTER_DIVIDER_LINE_X:
            draw_dashed_vertical_line(
                screen,
                YELLOW_CENTER_LINE,
                separator_line_x,
                road_scroll_y,
                CENTER_LINE_WIDTH,
            )
        else:
            draw_dashed_vertical_line(
                screen,
                WHITE_ROAD_EDGE,
                separator_line_x,
                road_scroll_y,
                LANE_SEPARATOR_LINE_WIDTH,
            )


def draw_car(screen, car_x, car_y, body_color, detail_color):
    """위에서 내려다본 자동차를 원하는 색상으로 그립니다."""

    # 자동차 전체 차체를 세로 사각형으로 그립니다.
    car_body = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
    pygame.draw.rect(screen, body_color, car_body)

    # 자동차 가장자리에 어두운 테두리를 그려 입체감을 줍니다.
    pygame.draw.rect(screen, detail_color, car_body, CAR_BORDER_WIDTH)

    # 앞유리는 자동차 위쪽에 있는 하늘색 사각형입니다.
    front_window = pygame.Rect(
        car_x + (CAR_WIDTH - CAR_WINDOW_WIDTH) // 2,
        car_y + 18,
        CAR_WINDOW_WIDTH,
        CAR_WINDOW_HEIGHT,
    )
    pygame.draw.rect(screen, SKY_BLUE_WINDOW, front_window)

    # 뒷유리는 자동차 아래쪽에 있는 하늘색 사각형입니다.
    rear_window = pygame.Rect(
        car_x + (CAR_WIDTH - CAR_WINDOW_WIDTH) // 2,
        car_y + CAR_HEIGHT - CAR_WINDOW_HEIGHT - 18,
        CAR_WINDOW_WIDTH,
        CAR_WINDOW_HEIGHT,
    )
    pygame.draw.rect(screen, SKY_BLUE_WINDOW, rear_window)

    # 차체 가운데에 어두운 장식선을 그려 자동차 모양을 더 잘 보이게 합니다.
    pygame.draw.line(
        screen,
        detail_color,
        (car_x + CAR_WIDTH // 2, car_y + 48),
        (car_x + CAR_WIDTH // 2, car_y + CAR_HEIGHT - 48),
        3,
    )

    # 왼쪽 앞바퀴를 검은색 사각형으로 그립니다.
    front_left_tire = pygame.Rect(
        car_x - CAR_TIRE_WIDTH,
        car_y + 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, front_left_tire)

    # 오른쪽 앞바퀴를 검은색 사각형으로 그립니다.
    front_right_tire = pygame.Rect(
        car_x + CAR_WIDTH,
        car_y + 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, front_right_tire)

    # 왼쪽 뒷바퀴를 검은색 사각형으로 그립니다.
    rear_left_tire = pygame.Rect(
        car_x - CAR_TIRE_WIDTH,
        car_y + CAR_HEIGHT - CAR_TIRE_HEIGHT - 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, rear_left_tire)

    # 오른쪽 뒷바퀴를 검은색 사각형으로 그립니다.
    rear_right_tire = pygame.Rect(
        car_x + CAR_WIDTH,
        car_y + CAR_HEIGHT - CAR_TIRE_HEIGHT - 18,
        CAR_TIRE_WIDTH,
        CAR_TIRE_HEIGHT,
    )
    pygame.draw.rect(screen, BLACK_TIRE, rear_right_tire)


class ObstacleCar:
    """앞으로 충돌 판정과 거리 센서에서 사용할 장애물 자동차 객체입니다."""

    def __init__(self, lane_index, world_y):
        # lane_index는 몇 번째 차선에 있는지 나타냅니다. 0부터 시작합니다.
        self.lane_index = lane_index

        # 차선 중앙 X좌표에서 자동차 너비의 절반을 빼면 자동차 왼쪽 X좌표가 됩니다.
        self.x = LANE_CENTER_X_LIST[lane_index] - (CAR_WIDTH // 2)

        # world_y는 도로 위의 고정된 위치입니다.
        # 카메라 스크롤 값과 더해서 실제 화면에 보이는 Y좌표를 계산합니다.
        self.world_y = world_y

    def get_screen_y(self, road_scroll_y):
        """도로 스크롤 값을 반영하여 화면에 그릴 Y좌표를 계산합니다."""

        return self.world_y + road_scroll_y

    def draw(self, screen, road_scroll_y):
        """파란색 장애물 자동차를 화면에 그립니다."""

        screen_y = self.get_screen_y(road_scroll_y)
        draw_car(screen, self.x, screen_y, BLUE_CAR_BODY, DARK_BLUE_CAR_DETAIL)


def main():
    """pygame을 시작하고 창이 닫힐 때까지 프로그램을 실행합니다."""

    # pygame 기능을 사용하기 전에 반드시 초기화합니다.
    pygame.init()

    # 1000x700 크기의 창을 만들고 제목을 설정합니다.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ASS V1.0 - Road")

    # FPS 제한을 위해 pygame 시계를 만듭니다.
    clock = pygame.time.Clock()

    # 거리 표시용 글꼴을 준비합니다.
    distance_font = pygame.font.SysFont(None, DISTANCE_TEXT_SIZE)

    # 자동차 위치는 움직일 수 있도록 변경 가능한 변수로 관리합니다.
    car_x = START_CAR_X
    car_y = START_CAR_Y

    # 장애물 자동차는 별도 객체로 만들어 관리합니다.
    # 지금은 움직이지 않지만, 나중에 충돌 판정과 센서 기능을 이 객체에 연결할 수 있습니다.
    obstacle_car = ObstacleCar(OBSTACLE_CAR_LANE_INDEX, OBSTACLE_CAR_WORLD_Y)

    # 도로 스크롤 값: 자동차가 앞으로 달린 거리를 차선 움직임으로 표현합니다.
    road_scroll_y = 0

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

        # 키보드 입력 확인: 현재 누르고 있는 키들을 한 번에 확인합니다.
        pressed_keys = pygame.key.get_pressed()

        is_moving_forward = pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]
        is_moving_backward = pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]

        # 이동 전 현재 위치에서 장애물이 위험 거리 안에 있는지 확인합니다.
        # 위험 거리라면 전진 입력만 무시하고, 후진/좌우 이동은 그대로 허용합니다.
        front_distance_before_move = calculate_front_distance(
            car_x,
            car_y,
            road_scroll_y,
            obstacle_car,
        )
        can_move_forward = not is_obstacle_too_close(front_distance_before_move)

        # 자동차 전진 입력 처리: 기준 위치 전까지는 자동차가 올라가고, 이후에는 차선이 내려갑니다.
        if is_moving_forward and can_move_forward:
            if car_y > CAR_CAMERA_LIMIT_Y:
                car_y -= CAR_SPEED
                car_y = max(car_y, CAR_CAMERA_LIMIT_Y)
            else:
                road_scroll_y += ROAD_SCROLL_SPEED

        # 후진 처리: 전진한 스크롤이 있으면 차선을 반대로 돌리고, 아니면 자동차가 아래로 내려갑니다.
        if is_moving_backward:
            if road_scroll_y > 0 and car_y <= CAR_CAMERA_LIMIT_Y:
                road_scroll_y -= ROAD_SCROLL_SPEED
                road_scroll_y = max(0, road_scroll_y)
            else:
                car_y += CAR_SPEED

        # 자동차 좌표 변경: A/D와 왼쪽/오른쪽 방향키는 같은 방식으로 좌우 이동합니다.
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            car_x -= CAR_SPEED
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            car_x += CAR_SPEED

        car_x, car_y = limit_car_position(car_x, car_y)

        # 이동이 끝난 현재 위치를 기준으로 앞쪽 장애물까지의 거리를 계산합니다.
        front_distance = calculate_front_distance(
            car_x,
            car_y,
            road_scroll_y,
            obstacle_car,
        )

        # 먼저 전체 화면을 초록색 배경으로 채웁니다.
        screen.fill(GREEN_BACKGROUND)

        # 배경 위에 도로와 노란색 중앙선을 그립니다.
        draw_road(screen, road_scroll_y)

        # 도로 위에 파란색 장애물 자동차를 먼저 그립니다.
        obstacle_car.draw(screen, road_scroll_y)

        # 장애물이 감지될 때만 센서 선을 그립니다.
        if front_distance is not None:
            draw_front_sensor_line(screen, car_x, car_y, obstacle_car, road_scroll_y)

        # 도로 위에 빨간색 플레이어 자동차를 그립니다.
        draw_car(screen, car_x, car_y, RED_CAR_BODY, DARK_RED_CAR_DETAIL)

        # 거리 감지 결과는 자동차와 도로를 그린 뒤 화면 위에 표시합니다.
        draw_distance_text(screen, distance_font, front_distance)

        # 지금까지 그린 내용을 실제 창에 보여줍니다.
        pygame.display.flip()

        # FPS 제한: 게임 루프가 초당 FPS번 정도 실행되도록 속도를 조절합니다.
        clock.tick(FPS)

    # pygame을 종료하여 사용한 자원을 정리합니다.
    pygame.quit()


# 이 파일을 직접 실행했을 때만 main 함수를 실행합니다.
if __name__ == "__main__":
    main()
