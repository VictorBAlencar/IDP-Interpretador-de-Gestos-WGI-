import calculo_distancia as util

def is_screenshot(landmark_list):
#Sinal de paz com o dedo indicador e do meio para cima. Anelar e mindinho para baixo
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
            util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 50
    )
