import tensorflow as tf
from easydict import EasyDict as edict
from tensorflow.python import keras
from tensorflow.python.keras import layers

from gans.models import sequential
from gans.models.gans import vanilla_gan
from gans.trainers import vanilla_gan_trainer

model_parameters = edict({
    'batch_size':                  256,
    'num_epochs':                  100,
    'buffer_size':                 10000,
    'latent_size':                 5,
    'learning_rate_generator':     0.0002,
    'learning_rate_discriminator': 0.0002,
    'save_images_every_n_steps':   1000
})

generator = sequential.SequentialModel(
    layers=[
        keras.Input(shape=[model_parameters.latent_size]),
        layers.Dense(units=15),
        layers.ELU(),
        layers.Dense(units=2, activation='linear'),
    ]
)

discriminator = sequential.SequentialModel(
    [
        keras.Input(shape=[2]),
        layers.Dense(units=25, activation='relu'),
        layers.Dense(units=2, activation='sigmoid'),
    ]
)

generator_optimizer = tf.keras.optimizers.Adam(
    learning_rate=model_parameters.learning_rate_generator,
    beta_1=0.5,
)
discriminator_optimizer = tf.keras.optimizers.Adam(
    learning_rate=model_parameters.learning_rate_discriminator,
    beta_1=0.5,
)

gan_trainer = vanilla_gan_trainer.VanillaGANTrainer(
    batch_size=model_parameters.batch_size,
    generator=generator,
    discriminator=discriminator,
    dataset_type='VANILLA_MNIST_MODEL_FUNCTION_X^2',
    generator_optimizer=generator_optimizer,
    discriminator_optimizer=discriminator_optimizer,
    continue_training=False,
    save_images_every_n_steps=model_parameters.save_images_every_n_steps,
)
vanilla_gan_model = vanilla_gan.VanillaGAN(
    model_parameters=model_parameters,
    generator=generator,
    discriminator=discriminator,
    gan_trainer=gan_trainer,
)


def generate_samples(num_samples):
    x = tf.random.uniform(shape=[num_samples]) - 0.5
    y = x * x
    data = tf.stack([x, y], axis=1)
    from matplotlib import pyplot as plt
    plt.scatter(data[:, 0], data[:, 1])
    return tf.data.Dataset. \
        from_tensor_slices(data). \
        shuffle(model_parameters.buffer_size). \
        batch(model_parameters.batch_size)


train_dataset = generate_samples(num_samples=500000)

vanilla_gan_model.fit(train_dataset)
