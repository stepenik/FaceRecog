import numpy as np
from PIL import Image as IM
import pylab

def mode_normalize( mode, high = 255 , low = 0) :
	MAX = np.max(mode)
	MIN = np.min(mode)

	#print "Mode MIN : " , MIN 
	#print "Mode MAX : " , MAX

 	mode_255 = mode

 	mode_255 -= float(MIN)
 	mode_255 /= float(MAX-MIN)

 	mode_255 *= (high - low)
 	mode_255 += low

	return mode_255



i = 0
m = 20 # number of images used to calculate mean

faces = []

for i in range(0,m,1) : #GW Bush
	faces.append( IM.open("../data/gwb_cropped/" + str(i+1) + ".jpg") )
'''
for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s1/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s2/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s3/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s4/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s5/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s6/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s7/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image

for i in range (0,m,1) : # m images
	faces.append( IM.open("../data/att_faces/s8/" + str(i+1) + ".pgm") ) # 92 x 112 PGM image
'''	


w,h = faces[0].size # get size (WxH) of first image in list, assuming all are same size!
#print w,h
N = len(faces) # number of faces
print "Number of face images : " , N

mean_array=np.zeros((h,w),np.float) # filling empty numpy array 92x112 with zeros


for face in faces :
    imarr=np.array(face,dtype=np.float) # converting each 'face image' into numpy array
    mean_array += imarr #adding up all the faces

mean_array /= N #calculating mean face

diff_array = [N] # diff_array = face - mean_array

for i in range(0,N,1) :
    diff_array.append(np.zeros((h,w),dtype=np.float)) # filling with zeros

for i in range(0,N,1) :
    diff_array[i] -= mean_array # ( face - mean_face ) for each image

flat_darray = np.zeros((N,h*w),dtype=np.float)
flat_marray = mean_array.flatten()

#print flat_darray.size
#print flat_marray.size


for i in range(0,N,1) :
	flat_darray[i]=(diff_array[i].flatten()) # converting NxHxW 3D array to Nx(HxW) 2D array i.e N rows for each face, of HxW columns


'''
PCA - 1 
'''

COV =  (np.dot(flat_darray,flat_darray.T)) #compute covariance matrix of non-zero eigenvectors

#print COV
#print COV.shape


eigenvalues,eigenvectors = np.linalg.eigh(COV) # get eigenvalues and eigenvectors
#print EVector.shape
#print e

# sorting eigenvalues in descending order
index_arr = np.argsort(-eigenvalues)
eigenvalues = eigenvalues[index_arr]

# sorting eigenvectors in ascending order of their eigenvalues 
eigenvectors = eigenvectors[:,index_arr]

#print flat_darray.shape
#print (flat_darray.T).shape

#tmp = (np.dot(flat_darray.T,eigenvectors)).T # ( (difference_vector).T x EVector ).T  - obtain eigenfaces [eigenfaces represent the largest similarities between some faces, and the most drastic differences between others]
V1 = np.dot(eigenvectors.T,flat_darray) # same as above

print flat_darray.shape
print eigenvectors.shape
print eigenvectors.T.shape


# V is the projection matrix 
#V1 = tmp [::-1] # reversing array, puts it in descending order - eigenvectors with most variance
#V = np.argsort(tmp,axis=0)



# S is the variance 
#S = e[::-1] # reversing eigenvalues as well, singular value decompisition = sqrt(eigenvalue) - PCA uses SVD
#print S
#S = np.sqrt(S)

mode1 = V1[0].reshape(h,w) # using first principal component
mode2 = V1[4].reshape(h,w)
mode3 = V1[9].reshape(h,w)
#print mode1.shape


mode_255 = mode_normalize(mode1)
mode_255_2 = mode_normalize(mode2)




'''
pylab.figure()
pylab.gray()
pylab.imshow(diff_array[0])

pylab.figure()
pylab.gray()
pylab.imshow(mean_array)
'''

pylab.figure()
pylab.gray()
pylab.imshow(mode_255)

pylab.figure()
pylab.gray()
pylab.imshow(mode_255_2)


'''
pylab.figure()
pylab.gray()
pylab.imshow(np.array(faces[0],dtype=np.float))
'''

'''
PCA - MATPLOTLIB
'''

from matplotlib.mlab import PCA

results = PCA(flat_darray.T) 
results_array = (results.Y.T)#[::-1]

#mode_PCA = (results.Y.T)[0].reshape(h,w)
#print mode_PCA.shape
mode_PCA = results_array[0].reshape(h,w)

mode_PCA = mode_normalize(mode_PCA)

print "-------------"

print "OurPCA: \n ", V1[0]

print "-------------"


print "OurPCA 2: \n ", V1[9]

print "-------------"

print "MATPLOTLIB PCA: \n ", results_array[0]

print "-------------"

print "OurPCA mode: \n " , mode1

print "-------------"

print "OurPCA mode 2: \n " , mode2

print "-------------"

print "MATPLOTLIB mode: \n " , mode_PCA

print "-------------"
#print results_array



pylab.figure()
pylab.gray()
pylab.imshow(mode_PCA)

pylab.show()

'''
# Round values in array and cast as 8-bit integer
arr=np.array(np.round(diff_array[0]),dtype=np.uint8)
#arr=np.array(np.round(mean_array),dtype=np.uint8)

# Generate, save and preview final image
out=IM.fromarray(arr,mode="L")
#out.save("../output/diff_face_s1_minus_s1234.png")
out.show()
'''