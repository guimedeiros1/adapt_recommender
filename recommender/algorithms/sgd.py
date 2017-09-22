import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from recommender.models import Rating

class FactMatrix:

    def sgd(self):
        # transform the Rating QuerySet into a pandas DataFrame
        df = pd.DataFrame(list(Rating.objects.all().values()))

        #################VERIFICAR PORQUE ESTÁ PEGANDO 403 FILMES AO INVÉS DE 407
        n_users = df.learner_id.max() #get the max user id
        n_items = df.movie_id.max()

        df = df.dropna(subset=['rating'])  # drop the lines where the user has not given a rating to the film (rating == NaN)

        train_data, test_data = train_test_split(df,test_size=0.25)

        train_data = pd.DataFrame(train_data)
        test_data = pd.DataFrame(test_data)

        # Create training and test matrix
        R = np.zeros((n_users+1, n_items+1)) #it is add +1 to match the bd indices
        for line in train_data.itertuples():
            R[line[4], line[6]] = line[8] #line[4] is the user_id // line[6] is the movie_id // line[8] is the user atributed rating

        T = np.zeros((n_users+1, n_items+1))
        for line in test_data.itertuples():
            T[line[4], line[6]] = line[8]

        # Index matrix for training data
        I = R.copy()
        I[I > 0] = 1
        # I[I == 0] = 0

        # Index matrix for test data
        I2 = T.copy()
        I2[I2 > 0] = 1
        # I2[I2 == 0] = 0

        # Predict the unknown ratings through the dot product of the latent features for users and items
        def prediction(P,Q):
            return np.dot(P.T,Q)


        lmbda = 0.1 # Regularisation weight
        k = 20  # Dimensionality of the latent feature space
        m, n = R.shape  # Number of users and items
        n_epochs = 1  # Number of epochs
        gamma=0.01  # Learning rate

        P = 3 * np.random.rand(k,m) # Latent user feature matrix
        Q = 3 * np.random.rand(k,n) # Latent movie feature matrix

        # Calculate the RMSE
        def rmse(I,R,Q,P):
            return np.sqrt(np.sum((I * (R - prediction(P,Q)))**2)/len(R[R > 0]))

        train_errors = []
        test_errors = []

        #Only consider non-zero matrix
        users,items = R.nonzero()
        for epoch in range(n_epochs):
            for u, i in zip(users,items):
                e = R[u, i] - prediction(P[:,u],Q[:,i])  # Calculate error for gradient
                P[:,u] += gamma * ( e * Q[:,i] - lmbda * P[:,u]) # Update latent user feature matrix
                Q[:,i] += gamma * ( e * P[:,u] - lmbda * Q[:,i])  # Update latent movie feature matrix
            train_rmse = rmse(I,R,Q,P) # Calculate root mean squared error from train dataset
            test_rmse = rmse(I2,T,Q,P) # Calculate root mean squared error from test dataset
            train_errors.append(train_rmse)
            test_errors.append(test_rmse)

        # # Check performance by plotting train and test errors
        # import matplotlib.pyplot as plt
        # get_ipython().magic('matplotlib inline')
        #
        # plt.plot(range(n_epochs), train_errors, marker='o', label='Training Data');
        # plt.plot(range(n_epochs), test_errors, marker='v', label='Test Data');
        # plt.title('SGD-WR Learning Curve')
        # plt.xlabel('Number of Epochs');
        # plt.ylabel('RMSE');
        # plt.legend()
        # plt.grid()
        # plt.show()

        # Calculate prediction matrix R_hat (low-rank approximation for R)
        # R = pd.DataFrame(R)
        R_hat=pd.DataFrame(prediction(P,Q))

        return R_hat

        # # Compare true ratings of user 17 with predictions
        # ratings = pd.DataFrame(data=R.loc[int(user_id),R.loc[int(user_id),:] > 0]).head(n=5)
        # ratings['Prediction'] = R_hat.loc[int(user_id),R.loc[int(user_id),:] > 0]
        # ratings.columns = ['Actual Rating', 'Predicted Rating']
        # return ratings

