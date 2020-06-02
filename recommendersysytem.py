sc
movielens = sc.textFile("path.data")
movielens.first()
movielens.count()


#Clean up the data by splitting it
#Movielens readme says the data is split by tabs and
#is user product rating timestamp
clean_data = movielens.map(lambda x:x.split('\t'))

#As an example, extract just the ratings to its own RDD
#rate.first() is 3
rate = clean_data.map(lambda y: int(y[2]))
rate.mean() 

#Extract just the users
users = clean_data.map(lambda y: int(y[0]))
users.distinct().count() 

#We don't have to extract data to its own RDD
#This command counts the distinct movies
#There are 1,682 movies
clean_data.map(lambda y: int(y[1])).distinct().count()

#Need to import  functions / objects from the MLlib
from pyspark.mllib.recommendation import MatrixFactorizationModel, Rating
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import LinearRegressionWithSGD

#We'll need to map the movielens data to a Ratings object 
#A Ratings object is made up of (user, item, rating)
mls = movielens.map(lambda l: l.split('\t'))
ratings = mls.map(lambda x: Rating(int(x[0]),\
    int(x[1]), float(x[2])))
    
#Need a training and test set
train, test = ratings.randomSplit([0.7,0.3],7856)

train.count() #70,005
test.count()

rank = 5 # Latent Factors to be made
numIterations = 100 # Times to repeat process
#Create the model on the training data
model = LinearRegressionWithSGD.train(train, rank, numIterations)

# Evaluate the model on testdata
# dropping the ratings on the tests data
testdata = test.map(lambda p: (p[0], p[1]))
predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
# joining the prediction with the original test dataset
ratesAndPreds = X_test.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)

# calculating error
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error = " + str(MSE))
