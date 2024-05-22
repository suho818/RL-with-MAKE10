import random
import numpy as np


class MAKE10:
    def __init__(self, matrix=None):
        self.score = 0
        if matrix is None:
            self.matrix = np.random.randint(1, 10, size=(9, 18))
        else:
            self.matrix = matrix
        self.attempt = 0
        self.log = 0

    def generate_matrix(self):
        return np.random.randint(1, 10, size=(9, 18))

    def _sum_rec(self, sub_matrix):
        return np.sum(sub_matrix)

    def _elim(self, coord1, coord2):
        self.attempt += 1
        r1, c1 = coord1
        r2, c2 = coord2

        start_row = min(r1, r2)
        end_row = max(r1, r2)
        start_column = min(c1, c2)
        end_column = max(c1, c2)

        sub_matrix = self.matrix[start_row:end_row + 1, start_column:end_column + 1]
        print(sub_matrix)
        if self._sum_rec(sub_matrix) == 10:
            self.score += np.count_nonzero(sub_matrix)
            self.matrix[start_row:end_row + 1, start_column:end_column + 1] = 0
    def coord_to_num(self, coord1, coord2):
        row1, col1 = coord1
        row2, col2 = coord2
        num1 = row1*18 + col1
        num2 = row2*18 + col2
        num = num1*162 + num2
        return num

    def num_to_coord(self, num):
        num1 = num // 162
        num2 = num % 162
        row1 = num1 // 18
        col1 = num1 % 18
        row2 = num2 // 18
        col2 = num2 % 18
        return (row1, col1), (row2, col2)
    def do(self, coord):
        row1, col1 = coord
        self._elim(row1, col1)

class Player:
    def __init__(self, game):
        self.game = game

    def choose_random_coordinates(self):
        # 무작위로 행과 열 인덱스 선택
        row1 = np.random.randint(0, 9)  # 첫 번째 좌표의 행 인덱스
        col1 = np.random.randint(0, 18)  # 첫 번째 좌표의 열 인덱스
        row2 = np.random.randint(0, 9)  # 두 번째 좌표의 행 인덱스
        col2 = np.random.randint(0, 18)  # 두 번째 좌표의 열 인덱스
        return (row1, col1), (row2, col2)

    def attention(self):
        # 시선을 한 좌표로 고정 - 무작위로 행과 열 선택
        row = np.random.randint(0, 9)
        col = np.random.randint(0, 18)
        return (row, col)

    def choose_second_coordinate(self, coord1):
        # 시선 고정한 점을 기준으로 거리에 따른 확률을 보정하여 두번째 좌표 선택
        row1, col1 = coord1
        distances = []

        for r in range(9):
            for c in range(18):
                distance = np.sqrt((r - row1) ** 2 + (c - col1) ** 2)
                if distance != 0:
                    distances.append(((r, c), distance))

        # 거리에 따른 확률분포 정규화
        total_distance = sum([1 / d for _, d in distances])
        probabilities = [(1 / d) / total_distance for _, d in distances]
        chosen_index = np.random.choice(len(distances), p=probabilities)
        return distances[chosen_index][0]

    def play(self, action):

        if action == 1:
            a, b = self.choose_random_coordinates()
        else:
            a = self.attention()
            b = self.choose_second_coordinate(a)
        self.game.do((a,b))
        return a,b


def txt_to_matrix(file_path):
    # 파일을 읽어와서 각 줄을 리스트로 저장
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 각 줄의 숫자를 요소로 갖는 리스트 생성
    matrix_list = []
    for line in lines:
        row = [int(num) for num in line.split()]
        matrix_list.append(row)

    # 리스트를 numpy 배열로 변환하여 반환
    matrix = np.array(matrix_list)
    return matrix

