import keras
#import numpy as np
from keras.models import Sequential
from keras.initializers import he_normal
from keras.layers.normalization import BatchNormalization
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, Activation,Flatten
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
import keras.backend as K
import tensorflow as tf
K.set_image_data_format('channels_last')
#K.set_learning_phase(1)
import matplotlib.pyplot as plt
#加载keras模块
#from keras import optimizers
from keras.optimizers import SGD, Adam, RMSprop, Adadelta
from keras.preprocessing.image import ImageDataGenerator
#from keras.utils.training_utils import multi_gpu_model   #导入keras多GPU函数
from sklearn import cross_validation,metrics
#from sklearn import svm
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_auc_score
import os
# 使用第一张与第三张GPU卡
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def new_loss(y_true,y_pred):
    
    y_pred /= tf.reduce_sum(y_pred,-1, True)
    y_pred=tf.clip_by_value(y_pred,1e-10,1.0-1e-10)
#    print(y_true.shape)
    a_0=-(y_true[:,0] * tf.log(y_pred[:,0]) + (1-y_true[:,0]) * tf.log(1-y_pred[:,0]))
    a_1=-(y_true[:,1] * tf.log(y_pred[:,1]) + (1-y_true[:,1]) * tf.log(1-y_pred[:,1]))
    a_2=-(y_true[:,2] * tf.log(y_pred[:,2]) + (1-y_true[:,2]) * tf.log(1-y_pred[:,2]))
    a_3=-(y_true[:,3] * tf.log(y_pred[:,3]) + (1-y_true[:,3]) * tf.log(1-y_pred[:,3]))
    a_4=-(y_true[:,4] * tf.log(y_pred[:,4]) + (1-y_true[:,4]) * tf.log(1-y_pred[:,4]))
    a_5=-(y_true[:,5] * tf.log(y_pred[:,5]) + (1-y_true[:,5]) * tf.log(1-y_pred[:,5]))
    a_6=-(y_true[:,6] * tf.log(y_pred[:,6]) + (1-y_true[:,6]) * tf.log(1-y_pred[:,6]))
    a_7=-(y_true[:,7] * tf.log(y_pred[:,7]) + (1-y_true[:,7]) * tf.log(1-y_pred[:,7]))
    a_8=-(y_true[:,8] * tf.log(y_pred[:,8]) + (1-y_true[:,8]) * tf.log(1-y_pred[:,8]))
    a_9=-(y_true[:,9] * tf.log(y_pred[:,9]) + (1-y_true[:,9]) * tf.log(1-y_pred[:,9]))
    a_10=-(y_true[:,10] * tf.log(y_pred[:,10]) + (1-y_true[:,10]) * tf.log(1-y_pred[:,10]))
    
    haha=1163/3331*a_0 + 154/3331*a_1 + 142/3331*a_2 + 313/3331*a_3 + 179/3331*a_4 + 195/3331*a_5 +339/3331*a_6 +163/3331*a_7 + 210/3331*a_8 + 141/3331*a_9 + 332/3331*a_10
    newloss=tf.reduce_mean(haha)
    return newloss

#
def auc(y_true,y_pred):
    
    auc=tf.py_func(roc_auc_score, [y_true, y_pred], tf.double)
#    K.get_session().run(tf.local_variables_initializer())
#    return tf.py_func(roc_auc_score, (y_true, y_pred), tf.double)
#    auc_1=tf.py_func(roc_auc_score, (y_true, y_pred), tf.double)
##    map_1=1./11*tf.py_func(average_precision_score, (y_true, y_pred), tf.double)
    return auc
#def auc(y_true, y_pred):
#    auc_1 = tf.metrics.auc(y_true[:,0], y_pred[:,0])[1]
##    map_1=tf.metrics.average_precision_at_k(y_true[:,1:],y_pred[:,1:], 10)
#    K.get_session().run(tf.local_variables_initializer())
#    return 0.7*auc_1 + 0.3*map_1   


#写一个LossHistory类，保存loss和acc
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}
 
    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))
 
    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))
 
    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()
# build model
model = Sequential()
weight_decay = 0.0001
dropout=0.5
# Block 1
model.add(Conv2D(64, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
             kernel_initializer=he_normal(), name='block1_conv1', input_shape=(499,499,3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
             kernel_initializer=he_normal(), name='block1_conv2'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool'))

# Block 2
#model.add(Conv2D(128, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block2_conv1'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
#model.add(Conv2D(128, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block2_conv2'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
#model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool'))

# Block 3
#model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block3_conv1'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
#model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block3_conv2'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
# model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block3_conv3'))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
#model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block3_conv4'))
#model.add(BatchNormalization())
##model.add(Activation('relu'))
#model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool'))

# Block 4
#model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block4_conv1'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
#model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block4_conv2'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
# model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block4_conv3'))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
#model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block4_conv4'))
#model.add(BatchNormalization())
##model.add(Activation('relu'))
#model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool'))

# Block 5
#model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block5_conv1'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
#model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block5_conv2'))
#model.add(BatchNormalization())
#model.add(Activation('relu'))
# model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block5_conv3'))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
#model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=keras.regularizers.l2(weight_decay),
#             kernel_initializer=he_normal(), name='block5_conv4'))
#model.add(BatchNormalization())
##model.add(Activation('relu'))
#model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool'))

# model modification for cifar-10
#model.add(Flatten(name='flatten'))
model.add(GlobalAveragePooling2D())
model.add(Dense(1080, use_bias=True, kernel_regularizer=keras.regularizers.l2(weight_decay),
            kernel_initializer=he_normal(), name='fc1'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(dropout))
model.add(Dense(1080, kernel_regularizer=keras.regularizers.l2(weight_decay),
            kernel_initializer=he_normal(), name='fc2'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(dropout))
model.add(Dense(11, kernel_regularizer=keras.regularizers.l2(weight_decay),
            kernel_initializer=he_normal(), name='fc3'))
model.add(BatchNormalization())
model.add(Activation('softmax'))

#G=4
#if G <= 1:
#    print("[INFO] training with 1 GPU...")
#    parallel_model = VGG19_model()
#
## otherwise, we are compiling using multiple GPUs
#else:
#    print("[INFO] training with {} GPUs...".format(G))
#    # we'll store a copy of the model on *every* GPU and then combine
#    # the results from the gradient updates on the CPU
#    with tf.device("/cpu:0"):
#        # initialize the model
#        model = VGG19_model()
#        # make the model parallel(if you have more than 2 GPU)
#    parallel_model = multi_gpu_model(model, gpus=G)
#    parallel_model.__setattr__('callback_model', model)


#parallel_model.__setattr__('callback_model', model)
adadelta=Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=1e-6)
#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
#adam=Adam(lr=0.06, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(loss=new_loss,optimizer=adadelta,metrics=['accuracy', auc])
model.summary()


# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        #rotation_range=180,
        rescale=1./255,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='constant',
        channel_shift_range=10,
        cval=0)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        'data/split_round2_part0',  # this is the target directory
        target_size=(499, 499),  # all images will be resized to 150x150
        batch_size=10,
        class_mode="categorical")  # since we use binary_crossentropy loss, we need binary labels

# this is a similar generator, for validation data
validation_generator = test_datagen.flow_from_directory(
        'data/split_round2_part4',
        target_size=(499, 499),
        batch_size=32,
        class_mode="categorical")
print(train_generator.class_indices)
print(validation_generator.class_indices)
#创建一个实例history
history = LossHistory()





checkpointer_1=ModelCheckpoint(filepath='VGG13_models/model.hdf5', monitor='val_auc', verbose=0, save_best_only=True, save_weights_only=False, mode='auto', period=1)
checkpointer=ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, verbose=0, mode='auto', epsilon=0.0001, cooldown=0, min_lr=0.00001)
#model.fit(X_train, Y_train, epochs = 1000, batch_size = 64,callbacks=[checkpointer,checkpointer_1,history],validation_split=0.14)
model.fit_generator(
        train_generator,
        epochs=2,
        verbose=1,
        validation_data=validation_generator,
        class_weight='auto',
        callbacks=[checkpointer,checkpointer_1,history],
        workers=4,
        shuffle=True)
#绘制acc-loss曲线
history.loss_plot('epoch')




