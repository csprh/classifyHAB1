"""
Train our RNN on extracted features or images.
"""
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from models import ResearchModels
from dataHAB import DataSet
import time
import os.path
import xml.etree.ElementTree as ET
import sys

def train(load_to_memory, inDir, dataDir,data_type, seqName, seq_length, model, image_shape=None,
          batch_size=32, nb_epoch=100):
    #import pdb; pdb.set_trace()
    #import pudb; pu.db
    # Helper: Save the model.

    checkpointer = ModelCheckpoint(
        filepath=os.path.join(dataDir, 'checkpoints', model + '-' + data_type + \
            '.{epoch:03d}-{val_loss:.3f}.hdf5'), verbose=1, save_best_only=True)
    # Helper: TensorBoard
    tb = TensorBoard(log_dir=os.path.join(dataDir, 'logs', model))

    # Helper: Stop when we stop learning.
    early_stopper = EarlyStopping(patience=100)

    # Helper: Save results.
    timestamp = time.time()
    csv_logger = CSVLogger(os.path.join(dataDir, 'logs', model + '-' + 'training-' + \
        str(timestamp) + '.log'))

    data = DataSet(seqName, seq_length, inDir, dataDir)

    # Get samples per epoch.
    # Multiply by 0.7 to attempt to guess how much of data.data is the train set.
    steps_per_epoch = (len(data.data) * 0.7) // batch_size

    if load_to_memory:
        # Get data.
        X, y = data.get_all_sequences_in_memory('train', data_type)
        X_test, y_test = data.get_all_sequences_in_memory('test', data_type)
    else:
        # Get generators.
        generator = data.frame_generator(batch_size, 'train', data_type)
        val_generator = data.frame_generator(batch_size, 'test', data_type)

    # Get the model.
    rm = ResearchModels(2, model, seq_length, None)

    # Fit!
    if load_to_memory:
        # Use standard fit.
        rm.model.fit(
            X,
            y,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1,
            callbacks=[tb, early_stopper, csv_logger],
            epochs=nb_epoch)
    else:
        rm.model.fit_generator(
            generator=generator,
            steps_per_epoch=steps_per_epoch,
            epochs=nb_epoch,
            verbose=1,
            callbacks=[tb, early_stopper, csv_logger, checkpointer],
            validation_data=val_generator,
            validation_steps=40,
            workers=4)

def main(argv):
    """These are the main training settings. Set each before running
    this file."""
    # model can be one of lstm, mlp
    #import pudb; pu.db

    if (len(argv)==0):
        xmlName = 'classifyHAB1.xml'
    else:
        xmlName = argv[0]

    #confg = getConfig(xmlName)

    tree = ET.parse(xmlName)
    root = tree.getroot()

    load_to_memory = 1
    for child in root:
        thisTag = child.tag
        thisText = child.text
        if thisTag == 'inDir':
            inDir = thisText
        elif thisTag == 'dataDir':
            dataDir = thisText
        elif thisTag == 'seqName':
            seqName = thisText
        elif thisTag == 'model':
            model = thisText
        elif thisTag == 'cnnModel':
            cnnModel = thisText
        elif thisTag == 'seqLength':
            seqLength = int(thisText)
        elif thisTag == 'batchSize':
            batchSize = int(thisText)
        elif thisTag == 'epochNumber':
            epochNumber = int(thisText)
        elif thisTag == 'lr':
            lr = float(thisText)
    train(load_to_memory, inDir, dataDir, 'features', seqName, seqLength, model, None,
          batchSize, epochNumber)

if __name__ == '__main__':
    main(sys.argv[1:])
