from .models import Img
from django.shortcuts import render
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from django.utils import timezone
from django.utils.timezone import localtime


# https://docs.djangoproject.com/ja/3.0/topics/http/file-uploads/


def index(request):
    now = localtime(timezone.now())
    print("qiulongquan_now={}".format(now))  # ���`���ڤ�now��print���Ƥߤ�
    # ��Ҫ���ݸ�index.html������ȫ���ŵ�context���棬�����ֵ����ͣ�Ȼ����index.html������ô洢��ֵ
    context = {'now': now, 'qiu': "customization"}
    return render(request, 'hello/index.html', context)


def prediction_process(img_paths):
    print(tf.__version__)
    classes = ['zero', 'one', 'two', 'three', 'four',
               'five', 'six', 'seven', 'eight', 'nine']
    prediction_results = []
    result_set = []
    # path to test image
    for img_path in img_paths:
        if img_path is not None:
            img = image.load_img(img_path, target_size=(100, 100))
            img_array = image.img_to_array(img)

            print(img_array.shape)
            # expected conv2d_input to have 4 dimensions, but got array with shape (100, 100, 3)
            # ��Ҫ���??(1, 100, 100, 3)
            pImg = np.expand_dims(img_array, axis=0) / 255
            print(pImg.shape)
            model_path = os.path.join("model", 'sign_language_vgg16_1.h5')
            sign_language_vgg16 = tf.keras.models.load_model(model_path)
            # sign_language_vgg16.summary()

            # [0]��ʾ�����ѡȡ��һ������??10��������֣�Ȼ���������
            prediction = sign_language_vgg16.predict(pImg)[0]

            print("qiulongquan_prediction={}".format(prediction))
            print(np.argmax(prediction))
            prediction_results.append(np.argmax(prediction))
            # [::-1]��������  [-5:]ȡǰ5��ֵ  argsort��ʾ���صĲ���ֵ������index
            top_indices = prediction.argsort()[-5:][::-1]
            result_five = [(classes[i], prediction[i]) for i in top_indices]
            result_set.append(result_five)
            for x in result_five:
                print(x)
        elif img_path is None:
            prediction_results.append("")
            result_set.append("")
    return prediction_results, result_set


def prediction(request):
    print("prediction image")
    if request.method == 'POST':
        checkbox_values = request.POST.getlist('checks[]')
        print("qiulongquan_POST_checkbox[]={}".format(checkbox_values))
        imgs = Img.objects.all()
        img_paths = []
        for i, img in enumerate(imgs):
            if str(i) in checkbox_values:
                print("img_path={}".format(os.path.join("media", img.img.name)))
                img_paths.append(os.path.join("media", img.img.name))
            else:
                img_paths.append(None)
        prediction_results, result_set = prediction_process(img_paths)
        content = {
            'imgs': imgs,
            # ����ǻ�ȡ��ǰʹ�õĶ˿ںŷ���??
            'port': request.META['SERVER_PORT'],
            # ����ǻ�ȡ��ǰhost�ķ����������Ѿ������˶˿ں�
            'host': request.get_host(),
            'img_paths': img_paths,
            'prediction_results': prediction_results,
            'result_set': result_set,
        }
        return render(request, 'hello/showing.html', content)


# �ڴ��ʹ��ļ���ʱ�򣬷�ֹ�ڴ�ר�ã�Ĭ���Ƽ�������?
def handle_uploaded_file(f, img_path):
    with open(img_path, 'wb') as destination:
        # �ڴ��ʹ��ļ���ʱ�򣬷�ֹ�ڴ�ר�ã�����ʹ��chunks����û��ʹ��read
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()


def uploadImg(request):
    """
    ͼƬ�ϴ�
    :param request:
    :return:
    """
    print("upload files and then show files")
    if request.method == 'POST':
        img_files = request.FILES.getlist("img")
        for img_file in img_files:
            name = img_file.name
            img_path = os.path.join("media/file", name)
            if os.path.exists(img_path.encode('utf-8')):
                print(str(img_path.encode('utf-8')) + "  exists.")
                continue
            else:
                print(str(img_path) + "  no exists.")
                handle_uploaded_file(img_file, img_path)
                Img(img=os.path.join("file", name), name=name).save()
                print("{} upload done.".format(name))
        # ���µ�����һ��urls�ַ���  views���Ե���htmlģ��Ҳ���Ե���urls�ַ���
    return render(request, 'hello/uploading.html')
    # return HttpResponsePermanentRedirect("/s/" + code + "/")


# ��������ַ����ǹ̶��洢��һ���ط�img���棬���ܸı�·�������Ƽ�
# from django.shortcuts import render
# from .models import Img
#
#
# def uploadImg(request):
#     """
#     ͼƬ�ϴ�
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         new_img = Img(
#             img=request.FILES.get('img'),
#             name=request.FILES.get('img').name
#         )
#         new_img.save()
#     return render(request, 'hello/uploading.html')


def showImg(request):
    """
    ͼƬ��ʾ
    :param request:
    :return:
    """
    print("qiulongquan_showImg_start")
    imgs = Img.objects.all()
    content = {
        'imgs': imgs,
        # ����ǻ�ȡ��ǰʹ�õĶ˿ںŷ���??
        'port': request.META['SERVER_PORT'],
        # ����ǻ�ȡ��ǰhost�ķ����������Ѿ������˶˿ں�
        'host': request.get_host(),
    }
    print("qiulongquan_content={}".format(content))
    for i in imgs:
        print("qiulongquan_url={}".format(i.img.url))
    return render(request, 'hello/showing.html', content)


def deleteImg(request):
    delete_list = request.POST.getlist('checks[]')
    print("qiulongquan_delete_list={}".format(delete_list))
    imgs = Img.objects.all()
    for img in imgs:
        if str(img.id) in delete_list:
            if os.path.exists(os.path.join('media', str(img.img.url))):
                # ɾ���ļ�����ʹ���������ַ�����
                os.remove(os.path.join('media', str(img.img.url)))
                print("%s delete completed" %
                      os.path.join('media', str(img.img.url)))
                Img.objects.get(id=img.id).delete()
            else:
                print('no such file:%s' %
                      os.path.join('media', str(img.img.url)))
    print("delete files done.")
    imgs = Img.objects.all()
    content = {
        'imgs': imgs,
        # ����ǻ�ȡ��ǰʹ�õĶ˿ںŷ���??
        'port': request.META['SERVER_PORT'],
        # ����ǻ�ȡ��ǰhost�ķ����������Ѿ������˶˿ں�
        'host': request.get_host(),
    }
    return render(request, 'hello/showing.html', content)
