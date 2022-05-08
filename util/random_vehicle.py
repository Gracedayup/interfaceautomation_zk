"""
随机生成6位数的车牌号
"""
import random
class RandomVehicle:

    def random_vehicle(self, lenth):
        self.lenth = lenth
        char0 = '京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽赣粤青藏川宁琼'
        char1 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
        char2 = '1234567890'
        len0 = len(char0)-1
        len1 = len(char1) - 1
        len2 = len(char2) - 1
        index = 0
        while index < 1:
            code = ''
            index0 = random.randint(1, len0)
            index1 = random.randint(1, len1)
            code += char0[index0]
            code += char1[index1]
            for i in range(1, lenth):
                index2 = random.randint(1, len2)
                code += char2[index2]
                index = index + 1
            return code

if __name__=='__main__':
    a = RandomVehicle().random_vehicle(7)
    print(a)


