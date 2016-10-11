__author__ = 's1668779'
# f = open("model-br.en", 'r')
# answer = {}
# for line in f:
#     k, v = line.strip().split('e')
#     answer[k.strip()] = v.strip()
#
# f.close()
#
# print(answer)
n=0
ff = ['a','b','c']
cc = ['a','b','c']
output = {}
with open('foo.txt', 'r') as v:
    for line in v:
        # print line
        line = line.strip('\n')

        line = str(line)
        f = line[1]+[2]+[3]
        print(f)

        # print line
        # ff = line
        # gg = ff[0]+ff[1]+ff[2]
        # cc = ff[4]+ff[5]+ff[6] #+ff[7]+ff[8]+ff[9]+ff[10]+ff[11]+ff[12]
        # g = int(cc)
        # print(g)
        # output[gg] = cc


        #print cc

print output