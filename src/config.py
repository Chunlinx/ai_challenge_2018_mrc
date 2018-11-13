import os
import tensorflow as tf
from prepro_test import prepro
from main import train, test
flags = tf.flags
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# home = os.path.expanduser("F:")
# train_file = os.path.join(home, "data", "squad", "train-v2.0.json")
# dev_file = os.path.join(home, "data", "squad", "dev-v2.0.json")
# test_file = os.path.join(home, "data", "squad", "dev-v2.0.json")
# glove_word_file = os.path.join(home, "data", "glove", "glove.840B.300d.txt")
# parser = argparse.ArgumentParser(description='PyTorch implementation for Multiway Attention Networks for Modeling '
#                                              'Sentence Pairs of the AI-Challenges')
#
# parser.add_argument('--log_dir', type=str, default='log/event')
# parser.add_argument('--save_dir', type=str, default='log/model')
# parser.add_argument('--answer_dir', type=str, default='log/answer')
#
# args = parser.parse_args()

flags.DEFINE_string("log_dir", 'log/event', "")
flags.DEFINE_string("save_dir", 'log/model', "")
flags.DEFINE_string("answer_dir", 'log/answer', "")
flags.DEFINE_string("mode", "train", "train/debug/test")


def get_args(config):
    target_dir = "data"
    log_dir = config.get_flag_value("log_dir", "log/event")
    save_dir = config.save_dir
    answer_dir = config.answer_dir
    train_record_file = os.path.join(target_dir, "train.tfrecords")
    dev_record_file = os.path.join(target_dir, "validation.tfrecords")
    test_record_file = os.path.join(target_dir, "test.tfrecords")
    word_emb_file = os.path.join(target_dir, "word_emb.json")
    train_eval = os.path.join(target_dir, "train_eval.json")
    dev_eval = os.path.join(target_dir, "validation_eval.json")
    test_eval = os.path.join(target_dir, "test_eval.json")
    dev_meta = os.path.join(target_dir, "dev_meta.json")
    test_meta = os.path.join(target_dir, "test_meta.json")
    word2idx_file = os.path.join(target_dir, "word2idx.json")
    answer_file = os.path.join(answer_dir, "answer_old.json")

    datadir = os.path.join("/search/work/input")
    train_file = os.path.join(datadir, "ai_challenger_oqmrc_train", "train.json")
    validation_file = os.path.join(datadir, "ai_challenger_oqmrc_validation", "dev.json")
    test_file = os.path.join(datadir, "data")
    wd_file = os.path.join(datadir, "chinesewd", "sgns.zhihu.bigram-char")
    # save_dict_file = os.path.join(target_dir, "extra_dict.txt")
    save_train_file = os.path.join(target_dir, "train_data_p.json")
    save_validation_file = os.path.join(target_dir, "dev_data_p.json")
    save_testa_file = os.path.join(target_dir, "test_data_p.json")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(answer_dir):
        os.makedirs(answer_dir)

    flags.DEFINE_string("target_dir", target_dir, "")
    # flags.DEFINE_string("log_dir", log_dir, "")
    # flags.DEFINE_string("save_dir", save_dir, "")
    flags.DEFINE_string("train_file", train_file, "")
    flags.DEFINE_string("dev_file", validation_file, "")
    flags.DEFINE_string("test_file", test_file, "")
    flags.DEFINE_string("wd_file", wd_file, "")

    flags.DEFINE_string("save_train_file", save_train_file,"")
    flags.DEFINE_string("save_validation_file", save_validation_file, "")
    flags.DEFINE_string("save_testa_file", save_testa_file, "")

    flags.DEFINE_string("train_record_file", train_record_file, "")
    flags.DEFINE_string("dev_record_file", dev_record_file, "")
    flags.DEFINE_string("test_record_file", test_record_file, "")
    flags.DEFINE_string("word_emb_file", word_emb_file, "")
    flags.DEFINE_string("train_eval_file", train_eval, "")
    flags.DEFINE_string("dev_eval_file", dev_eval, "")
    flags.DEFINE_string("test_eval_file", test_eval, "")
    flags.DEFINE_string("dev_meta", dev_meta, "")
    flags.DEFINE_string("test_meta", test_meta, "")
    flags.DEFINE_string("word2idx_file", word2idx_file, "")
    flags.DEFINE_string("answer_file", answer_file, "")

    flags.DEFINE_integer("glove_char_size", 94, "Corpus size for Glove")
    flags.DEFINE_integer("glove_word_size", int(2.2e6), "Corpus size for Glove")
    flags.DEFINE_integer("glove_dim", 300, "Embedding dimension for Glove")
    flags.DEFINE_integer("char_dim", 8, "Embedding dimension for char")

    flags.DEFINE_integer("para_limit", 500, "Limit length for paragraph")
    flags.DEFINE_integer("ques_limit", 50, "Limit length for question")
    flags.DEFINE_integer("alter_limit", 10, "Limit length for each alter")

    flags.DEFINE_integer("test_para_limit", 500,
                        "Max length for paragraph in test")
    flags.DEFINE_integer("test_ques_limit", 50, "Max length of questions in test")
    flags.DEFINE_integer("char_limit", 16, "Limit length for character")
    flags.DEFINE_integer("word_count_limit", -1, "Min count for word")
    flags.DEFINE_integer("char_count_limit", -1, "Min count for char")
    # flags.DEFINE_string("char2idx_file", char2idx_file, "")
    # flags.DEFINE_string("char_emb_file", char_emb_file, "")


    flags.DEFINE_integer("capacity", 15000, "Batch size of dataset shuffle")
    flags.DEFINE_integer("num_threads", 4, "Number of threads in input pipeline")
    flags.DEFINE_boolean("use_cudnn", True, "Whether to use cudnn (only for GPU)")
    flags.DEFINE_boolean("is_bucket", False, "Whether to use bucketing")
    flags.DEFINE_list("bucket_range", [40, 361, 40], "range of bucket")

    flags.DEFINE_integer("batch_size", 64, "Batch size")
    flags.DEFINE_integer("num_steps", 75000, "Number of steps")
    flags.DEFINE_integer("checkpoint", 1000, "checkpoint for evaluation")
    flags.DEFINE_integer("period", 100, "period to save batch loss")
    flags.DEFINE_integer("val_num_batches", 150, "Num of batches for evaluation")
    flags.DEFINE_float("init_lr", 0.5, "Initial lr for Adadelta")
    flags.DEFINE_float("keep_prob", 0.7, "Keep prob in rnn")
    flags.DEFINE_float("ptr_keep_prob", 0.7, "Keep prob for pointer network")
    flags.DEFINE_float("grad_clip", 5.0, "Global Norm gradient clipping rate")
    flags.DEFINE_integer("hidden", 128, "Hidden size")
    flags.DEFINE_integer("char_hidden", 100, "GRU dim for char")
    flags.DEFINE_integer("patience", 3, "Patience for lr decay")


    flags.DEFINE_float("loss_theta", 0.1, "loss theta")


def main(_):
    config = flags.FLAGS
    get_args(config)
    if config.mode == "train":
        train(config)
    elif config.mode == "prepro":
        prepro(config)
    elif config.mode == "debug":
        config.num_steps = 1
        config.val_num_batches = 1
        config.checkpoint = 1
        config.period = 1
        train(config)
    elif config.mode == "test":
        test(config)
    #
    # elif config.mode == "predict":
    #     predict(config)
    else:
        print("Unknown mode")
        exit(0)


if __name__ == "__main__":
    tf.app.run()
