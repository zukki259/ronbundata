
import json
import os
import sys

class rectangle:
    def __init__(self,vertices):
        if len(vertices)>0:
            left=vertices[0][0]
            right=vertices[0][0]
            top=vertices[0][1]
            bottom=vertices[0][1]
            for v in vertices:
                x=v[0]
                y=v[1]
                if x<left:
                    left=x
                if x>right:
                    right=x
                if y<top:
                    top=y
                if y>bottom:
                    bottom=y
            self.l=left
            self.r=right
            self.t=top
            self.b=bottom
            self.height=bottom-top
            self.width=right-left
            self.center=((left+right)/2,(top+bottom)/2)
    def ind_line_row(self):
        top=self.t
        bottom=self.b
        center=self.center[1]
        error=self.height*0.1
        ind_top=lambda y: abs(top-y)<error
        ind_bottom=lambda y: abs(bottom-y)<error
        ind_center=lambda t,b: ((t<center) and (b>center))or((top<(t+b)/2)and(bottom>(t+b)/2))
        return lambda rect:ind_top(rect.t) or ind_bottom(rect.b) or ind_center(rect.t,rect.b)
    def ind_line_column(self):
        left=self.l
        right=self.r
        center=self.center[0]
        error=self.width*0.1
        ind_left=lambda x: abs(left-x)<error
        ind_right=lambda x: abs(right-x)<error
        ind_center=lambda l,r: ((l<center) and (r>center))or((left<(l+r)/2)and(right>(l+r)/2))
        return lambda rect:ind_left(rect.l) or ind_right(rect.r) or ind_center(rect.l,rect.r)

class wordbox:
    def __init__(self,word,vertices):
        #import pdb;pdb.set_trace()
        self.rect=rectangle(vertices)
        self.word=word

def print_result(rows,columns):
    rows=[[w.word for w in row] for row in rows]
    print(rows)
    columns=[[w.word for w in column] for column in columns]
    print(columns)

def main(filename):
    f=open(filename,'r')
    json_data=json.load(f)
    wb=[]
    words=json_data["responses"][0]["textAnnotations"]
    for w in words:
        if '\n' in w["description"]:
            continue
        else:
            word=w["description"]
            vertices_dict=w["boundingPoly"]["vertices"]
            vertices=[]
            for v in vertices_dict:
                vertices.append([v['x'],v['y']])
            #import pdb;pdb.set_trace()
            wb_tmp=wordbox(word,vertices)
            wb.append(wb_tmp)
    f.close()
    rows=[]
    l=sorted(wb,key=lambda x:x.rect.t)
    key=l[0].rect.ind_line_row()
    row=[]
    for w in l:
        if key(w.rect):
            row.append(w)
        else:
            row.sort(key=lambda x:x.rect.l)
            rows.append(row)
            key=w.rect.ind_line_row()
            row=[w]
    columns=[]
    l=sorted(wb,key=lambda x:x.rect.l)
    key=l[0].rect.ind_line_column()
    column=[]
    for w in l:
        if key(w.rect):
            column.append(w)
        else:
            column.sort(key=lambda x:x.rect.t)
            columns.append(column)
            key=w.rect.ind_line_column()
            column=[w]
    return rows,columns

if __name__ == '__main__':
    filename=sys.argv[1]
    rows,columns=main(filename)
    print_result(rows,columns)
