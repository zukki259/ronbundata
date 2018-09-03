import sys
import os
from abbreviations import schwartz_hearst

def preprocess_file(f):
    buffer=''
    for i in f:
        buffer+=i
    buffer=buffer.replace('\n\n','')
    buffer=buffer.replace('- ','-')
    buffer=buffer.split('\n')
    for x in buffer:
        if not x == '':
            yield x
        else:
            pass

def main(file,mode):
    dict_abbr={}
    head=False
    t=[]

    for l in preprocess_file(file):
        i=l.split('\t')
        if head==False:
            head=True
        else:
            if len(i)<1:
                import pdb; pdb.set_trace()
                continue
            else:
                t.append(i)
                '''document+="\n"+i[3] '''
    dict_abbr=schwartz_hearst.extract_abbreviation_definition_pairs(tagged_text=t)
    return dict_abbr

def convert_dict(d,fnamelist):
    l=list()
    for i in fnamelist:
        abbrs=d[i].keys()
        abbr_dict=d[i]
        for j in abbrs:
            p=abbr_dict[j]
            l.append([i,j,p[0],p[1]])
    return l

def output_tsv(l,out_fd):
    for line in l:
        t="\t".join(line)
        out_fd.write(t+'\n')


def main_dir(dirname):
    dict_file=dict()
    fnamelist=list()
    iter_files=os.listdir(dirname)
    for i in iter_files:
        title,ext=os.path.splitext(i)
        if ext!='.ss':
            continue
        f=open(os.path.join(dirname,i),'r')
        dict_file[title]=main(f,'ss')
        f.close()
        fnamelist.append(title)
    l=convert_dict(dict_file,fnamelist)
    outfile=open('./{}.out'.format(os.path.basename(dirname)),'w')
    output_tsv(l,outfile)
    outfile.close()

if __name__=='__main__':
    if len(sys.argv)==1:
        print('USAGE: python {} [file]'.format(sys.argv[0]))
    else:
        if os.path.isdir(sys.argv[1]):
            main_dir(sys.argv[1])
        elif os.path.isfile(sys.argv[1]):
            fname,ext=os.path.splitext(sys.argv[1])
            if ext=='.ss':
                f=open(sys.argv[1],'r')
                main(f,'ss')
            else:
                print('ERROR: {} file is not supported.'.format(ext))

else:
    pass

