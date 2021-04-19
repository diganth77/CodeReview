import math
import sys
train_dataset=sys.argv[1]
test_dataset=sys.argv[2]
def vij(u_m_d,v_avg,v_ij):
    for i in u_m_d:
        v=0
        Ii=len(u_m_d[i])
        for j in u_m_d[i]:
            v+=float(u_m_d[i][j])
        v_ij[i]=v
        v_avg[i]=v/float(Ii)   
    return v_avg,v_ij

def w_a_i(u_m_d,v_avg,v_ij):
    w=dict()
    k=0
    val=0
    
    for a in u_m_d:
        for i in u_m_d:
            num=0
            one=0
            two=0
            if a!=i:
                c1=a+"-"+i
                c2=i+"-"+a
                if c1 in w or c2 in w:
                    continue
                else:
                    for m in u_m_d[a]:
                        if m in u_m_d[i]:
                            num+=(v_ij[a]-v_avg[a])*(v_ij[i]-v_avg[i])
                            one+=((v_ij[a]-v_avg[a])**2)
                            two+=((v_ij[i]-v_avg[i])**2)
                    denom=math.sqrt(one*two)
                    cal=0
                    if denom==0:
                        cal=0
                    else:
                        cal=num/float(denom)
                    w[c1]=cal  
    for h in w:
        val+=abs(w[h])
    if val>0:
        k=1/float(val)
    return w,k

def predict(u_m_d,v_avg,v_ij,w,k,user_test):
    weight=0
    count=0
    numerator=0
    mean_abs_error=0
    root_mean_sqr_error=0
    rmsd_num=0
    for a in user_test: 
        for m in user_test[a]:
            summation=0
            for i in u_m_d:
                if a!=i and m in u_m_d[i]:
                    cond1=a+"-"+i
                    cond2=i+"-"+a
                    weight=0
                    if cond1 in w:
                        weight=w[cond1]
                    elif cond2 in w:
                        weight=w[cond2]
                    if weight!=0:
                        summation+=weight*(float(u_m_d[i][m])-v_avg[i])
            if a in v_avg:
                predi_aj=v_avg[a]+k*summation
                count+=1
                actual_rating=float(user_test[a][m])
                numerator+=abs(predi_aj-actual_rating)
                rmsd_num+=((predi_aj-actual_rating)**2)
    mean_abs_error=numerator/float(count)
    root_mean_sqr_error=math.sqrt(rmsd_num/float(count))
    return mean_abs_error,root_mean_sqr_error
            
def main():
    
    f = open(train_dataset, "r")
    meanAbsError,rootMeanSqrError=0,0
    v_avg=dict()
    v_ij=dict()
    m_r_d=dict()
    u_m_d=dict()
    movie_rating=dict()
    user_test=dict()
    for x in f:
        x= x.strip()
        li=(x.split(","))
#        li[-1]=li[-1].strip()
        if li[1] in u_m_d:
            m_r_d=u_m_d[li[1]]
            m_r_d[li[0]]=li[2]
        else:
            m_r_d=dict()
            m_r_d[li[0]]=li[2]
            u_m_d[li[1]]=m_r_d
    vij(u_m_d,v_avg,v_ij)
    w,k=w_a_i(u_m_d,v_avg,v_ij)
    f1=open(test_dataset, "r")
    for y in f1:
        y=y.strip()
        li1=(y.split(","))
        if li1[1] in user_test:
            movie_rating=user_test[li1[1]]
            movie_rating[li1[0]]=li1[2]
        else:
            movie_rating=dict()
            movie_rating[li1[0]]=li1[2]
            user_test[li1[1]]=movie_rating
    meanAbsError,rootMeanSqrError=predict(u_m_d,v_avg,v_ij,w,k,user_test)
    print("Mean absolute error-->"+str(meanAbsError))
    print("Root mean squared error-->"+str(rootMeanSqrError))
            
        
    
if __name__=="__main__":
    main()
        
    
    