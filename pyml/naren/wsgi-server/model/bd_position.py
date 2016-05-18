import utils
import traceback
import generate_feature1

try:

    generate_feature1.generate_train(data_path='test', pos_id=59702)

except:
    traceback.print_exc()
