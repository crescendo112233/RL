import random
import string


class p_tree:
    def __init__(self, BV_length=10, max_video_quantity=1000):
        self.plt = {
            "top_tag": ["番剧", "动画", "鬼畜", "舞蹈"],
            "sub_tag": [
                ["资讯", "官方延伸"],  # 番剧
                ["MAD·AMV", "MMD·3D", "短片·手书", "配音", "手办·模玩", "动漫杂谈", "综合"],  # 动画
                ["鬼畜调教 ", "音MAD", "人力VOCALOID", "鬼畜剧场", "教程演示"],  # 鬼畜
                ["宅舞", "街舞", "明星舞蹈", "国风舞蹈", "手势·网红舞", "舞蹈综合", "舞蹈教程"],  # 舞蹈
                        ],
        }
        self.BV_length = BV_length
        self.max_video_quantity = max_video_quantity
        self.video_quantity = 0

        len1 = len(self.plt.get("top_tag"))
        self.top_request = [0 for _ in range(len1)]
        self.top_tag_length = len1

        self.sub_request = []
        self.sub_valid = []
        self.content = []
        sub_tag = self.plt.get("sub_tag")
        len2 = len(sub_tag)
        for i in range(len2):
            self.sub_request.append([0 for _ in range(len(sub_tag[i]))])
            self.sub_valid.append([1 for _ in range(len(sub_tag[i]))])
            self.content.append([[] for _ in range(len(sub_tag[i]))])

    def reset(self):
        self.video_quantity = 0
        self.top_request = [0 for _ in range(self.top_tag_length)]
        self.sub_request.clear()
        self.sub_valid.clear()
        self.content.clear()
        sub_tag = self.plt.get("sub_tag")
        len2 = len(sub_tag)
        for i in range(len2):
            self.sub_request.append([0 for _ in range(len(sub_tag[i]))])
            self.sub_valid.append([1 for _ in range(len(sub_tag[i]))])
            self.content.append([[] for _ in range(len(sub_tag[i]))])

    def add_video(self, index):  # index = [top_tag_index,sub_tag_index,"BV"]
        assert self.sub_valid[index[0]][index[1]] == 1, "add_video_by_index_fail: invalid sub tag"
        assert index[2] not in self.content[index[0]][index[1]], "add_video_by_index_fail: video not exist"
        # refresh list: request,content
        self.content[index[0]][index[1]].append(index[2])
        self.top_request[index[0]] += 1
        self.sub_request[index[0]][index[1]] += 1
        self.video_quantity += 1

    def remove_video(self, index):  # index = [top_tag_index,sub_tag_index,"BV"]
        assert self.sub_valid[index[0]][index[1]] == 1, "remove_video_by_index_fail: invalid sub tag"
        assert index[2] in self.content[index[0]][index[1]], "remove_video_by_index_fail: video not exist"
        # don't modify request
        self.content[index[0]][index[1]].remove(index[2])
        self.video_quantity -= 1

    def request_video(self, index):  # index = [top_tag_index,sub_tag_index,"BV"]
        assert self.sub_valid[index[0]][index[1]] == 1, "request_video_by_index: invalid sub tag"
        assert index[2] in self.content[index[0]][index[1]], "request_video_by_index: video not exist"
        # only modify request
        self.top_request[index[0]] += 1
        self.sub_request[index[0]][index[1]] += 1

    def randomly_remove_video_from_invalid_tag(self):
        flag = True
        sub_invalid_index = []
        for i in range(self.top_tag_length):
            for j in range(len(self.sub_valid[i])):
                if self.sub_valid[i][j] == 0:
                    sub_invalid_index.append((i, j))
        assert len(sub_invalid_index) != 0, "random_remove_from_invalid_tag: no invalid tag"
        while flag:
            location = random.choice(sub_invalid_index)
            if len(self.content[location[0]][location[1]]) != 0:
                video = random.choice(self.content[location[0]][location[1]])
                self.content[location[0]][location[1]].remove(video)
                self.video_quantity -= 1
                return video

    def add_branch(self, branch):  # branch = [top_tag_index,sub_tag_index]
        assert self.sub_valid[branch[0]][branch[1]] == 0, "add_branch: valid sub tag"
        self.sub_valid[branch[0]][branch[1]] = 1

    def remove_branch(self, branch):  # branch = [top_tag_index,sub_tag_index]
        assert self.sub_valid[branch[0]][branch[1]] == 1, "remove_branch: invalid sub tag"
        self.sub_valid[branch[0]][branch[1]] = 0

    def get_all_action_in_current_state(self):  # add branch / remove branch
        actions = []
        for i in range(self.top_tag_length):
            for j in range(len(self.sub_valid[i])):
                if self.sub_valid[i][j] == 1:
                    actions.append((i, j, 0))  # remove branch which valid
                if self.sub_valid[i][j] == 0:
                    actions.append((i, j, 1))  # add branch which invalid
        return actions

    def randomly_init_branch(self):
        for i in range(self.top_tag_length):
            for j in range(len(self.sub_valid[i])):
                if random.choice([0, 1]) == 0:
                    self.remove_branch([i, j])

    def get_state(self):
        state = []
        for i in range(self.top_tag_length):
            for j in range(len(self.sub_valid[i])):
                state.append((i, j, self.sub_valid[i][j], self.sub_request[i][j]))
        return state

    def randomly_add_video(self, n):  # for test
        sub_valid_index = []
        video_list = []
        for i in range(self.top_tag_length):
            for j in range(len(self.sub_valid[i])):
                if self.sub_valid[i][j] == 1:
                    sub_valid_index.append((i, j))
        assert len(sub_valid_index) != 0, "random_add_video: no valid tag"
        characters = string.ascii_lowercase + string.digits
        for _ in range(n):
            location = random.choice(sub_valid_index)
            video = "".join(random.choice(characters) for _ in range(self.BV_length))
            video_list.append((location[0], location[1], "BV" + video))
        for element in video_list:
            self.add_video(element)
