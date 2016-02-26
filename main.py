import cv2
import sys
import numpy as np
from random import randint


##Command line arguments extraction

if(len(sys.argv) <2):
    print 'Error'
else:
	Input_Image=sys.argv[1];

if(len(sys.argv) >2):
    H=int(sys.argv[2]) # H Parameter
    itr=float(sys.argv[3]) # Threshold
else:
    H=60 # H Parameter
    itr=0.25 # Threshold
    
## Image Reading
aimg = cv2.imread(Input_Image,1);

p, q = aimg.shape[:2]
img=cv2.resize(aimg,(q,p));
size=p,q,3
#outPut Image
out_img = np.zeros(size,dtype=np.uint8)
cv2.imshow("Original Image",aimg);

h, w = img.shape[:2]

num=h*w;
print h,w

## Re-arrangement of the image into a feature vector matrix
ref = np.zeros(shape=(num,5));
nref = np.zeros(shape=(num,5));

val = np.zeros(num);
m = np.zeros(5);
mK = np.zeros(5);
ctr=0;

for i in range(h):
    for j in range(w):
        ref[ctr][0]=img[i][j][0];
        ref[ctr][1]=img[i][j][1];
        ref[ctr][2]=img[i][j][2];
        ref[ctr][3]=i;
        ref[ctr][4]=j;
        ctr=ctr+1;

print ctr,h,w
k=ctr-1;

## Get mean and threshold outputs

# Function for estimating eucledian distance
def distanceH(refa,refb):
    dis = np.power((refa[0]-refb[0]),2) + np.power((refa[1]-refb[1]),2) + np.power((refa[2]-refb[2]),2) + np.power((refa[3]-refb[3]),2) + np.power((refa[4]-refb[4]),2);
    dis=np.sqrt(dis);
    return dis


#Random number generation for obtaining pixel iteration



flag=0;

while (k>0):
 
    ##Main Calculations
    
    if(flag==1):
        mK[0]=m[0];    
        mK[1]=m[1];    
        mK[2]=m[2];
        mK[3]=m[3];
        mK[4]=m[4];
    else:
        ptr=randint(0,k)
        mK[0]=ref[ptr][0];    
        mK[1]=ref[ptr][1];    
        mK[2]=ref[ptr][2];
        mK[3]=ref[ptr][3];
        mK[4]=ref[ptr][4];          
                  
    count=0;
    sumR=0;
    sumG=0;
    sumB=0;
    sumX=0;
    sumY=0;
  
    for i in range(k+1):
        disH=distanceH(mK,ref[i]);
            
        if(disH < H):
            #print disH;
            sumR=sumR+ref[i][0];
            sumG=sumG+ref[i][1];
            sumB=sumB+ref[i][2];
            sumX=sumX+ref[i][3];
            sumY=sumY+ref[i][4];
            val[count]=i
            count=count+1;
                
    #Mean calculation
    m[0]=np.floor(sumR/count);
    m[1]=np.floor(sumG/count);
    m[2]=np.floor(sumB/count);
    m[3]=np.floor(sumX/count);
    m[4]=np.floor(sumY/count);
    
    #Mean Shift estimation
    sumR=abs( m[0]-mK[0] );
    sumG=abs( m[1]-mK[1] );
    sumB=abs( m[2]-mK[2] );
    sumX=abs( m[3]-mK[3] );
    sumY=abs( m[4]-mK[4] );
    #mean calc
    disH = np.power(sumR,2) + np.power(sumG,2) + np.power(sumB,2) + np.power(sumX,2) + np.power(sumY,2);
    disH=np.sqrt(disH);
    
    if(disH<itr):
        #print dis
        flag=0
        mind=500;
        for i in range(count):
            di=np.power((ref[val[i]][0] - m[0]),2) + np.power((ref[val[i]][1] - m[1]),2) + np.power((ref[val[i]][2] - m[2]),2) + np.power((ref[val[i]][3] - m[3]),2) + np.power((ref[val[i]][4] - m[4]),2);
            di=np.sqrt(di);
            if(di<mind):
                mind=di;
                nVal=i;
        nR=img[ref[val[nVal]][3]][ref[val[nVal]][4]][0]; 
        nG=img[ref[val[nVal]][3]][ref[val[nVal]][4]][1];
        nB=img[ref[val[nVal]][3]][ref[val[nVal]][4]][2];   
        for i in range(count):
            out_img[ref[val[i]][3]][ref[val[i]][4]][0]=m[0];
            out_img[ref[val[i]][3]][ref[val[i]][4]][1]=m[1];
            out_img[ref[val[i]][3]][ref[val[i]][4]][2]=m[2];
        
            ref[val[i]][0]=-1;
            
        ctr=0;
            
        for i in range(k):
            if(ref[i][0] != -1):
                nref[ctr]=ref[i];
                ctr=ctr+1;    
        k=k-count;  
        for i in range(k):
                ref[i]=nref[i];             
    else:
        flag=1;         
    
print "Done"
#stop = timeit.default_timer()
cv2.imshow("Output Image",out_img)
#print stop - start 