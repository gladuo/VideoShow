# coding=utf-8

import json

json_str = '{"status": "Succeeded", "progress": 100, "createdDateTime": "2016-10-15T11:51:10.1684611Z", "lastActionDateTime": "2016-10-15T11:51:24.061298Z", "processingResult": "{\"version\":1,\"timescale\":1e+006,\"offset\":0,\"framerate\":29.97,\"width\":320,\"height\":240,\"fragments\":[{\"start\":0,\"duration\":2002000,\"interval\":500500,\"events\":[[{\"windowFaceDistribution\":{\"neutral\":0,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0}}],[{\"windowFaceDistribution\":{\"neutral\":0,\"happiness\":1,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.328942,\"happiness\":0.635211,\"surprise\":0.0124317,\"sadness\":0.00691114,\"anger\":0.00523566,\"disgust\":0.00803125,\"fear\":0.00092767,\"contempt\":0.00230928}}],[{\"windowFaceDistribution\":{\"neutral\":0,\"happiness\":1,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.25043,\"happiness\":0.425982,\"surprise\":0.170771,\"sadness\":0.0661583,\"anger\":0.03056,\"disgust\":0.00592418,\"fear\":0.0493396,\"contempt\":0.000834472}}],[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.347778,\"happiness\":0.163092,\"surprise\":0.211765,\"sadness\":0.0763898,\"anger\":0.0770464,\"disgust\":0.00433616,\"fear\":0.11751,\"contempt\":0.00208267}}]]},{\"start\":2002000,\"duration\":2002000,\"interval\":500500,\"events\":[[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.530015,\"happiness\":0.0726679,\"surprise\":0.301932,\"sadness\":0.0520441,\"anger\":0.0103841,\"disgust\":0.00669409,\"fear\":0.0243965,\"contempt\":0.00186633}}],[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.727851,\"happiness\":0.059978,\"surprise\":0.181374,\"sadness\":0.0105837,\"anger\":0.0057003,\"disgust\":0.00254388,\"fear\":0.00855763,\"contempt\":0.00341161}}],[{\"windowFaceDistribution\":{\"neutral\":0,\"happiness\":0,\"surprise\":1,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.410669,\"happiness\":0.0436912,\"surprise\":0.482582,\"sadness\":0.027405,\"anger\":0.0154654,\"disgust\":0.0046866,\"fear\":0.0113538,\"contempt\":0.0041467}}],[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.477684,\"happiness\":0.0716304,\"surprise\":0.379425,\"sadness\":0.0411227,\"anger\":0.0106194,\"disgust\":0.00755802,\"fear\":0.00850699,\"contempt\":0.0034538}}]]},{\"start\":4004000,\"duration\":500500,\"interval\":500500,\"events\":[[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.903967,\"happiness\":0.0460066,\"surprise\":0.0235977,\"sadness\":0.00980339,\"anger\":0.00743151,\"disgust\":0.00278017,\"fear\":0.000797115,\"contempt\":0.00561624}}]]},{\"start\":4504500,\"duration\":500500,\"interval\":500500,\"events\":[[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.962392,\"happiness\":0.00922101,\"surprise\":0.0124581,\"sadness\":0.00872264,\"anger\":0.00336315,\"disgust\":0.000966459,\"fear\":0.000921979,\"contempt\":0.00195459}}]]},{\"start\":5005000,\"duration\":5672333,\"interval\":5672333,\"events\":[[{\"windowFaceDistribution\":{\"neutral\":1,\"happiness\":0,\"surprise\":0,\"sadness\":0,\"anger\":0,\"disgust\":0,\"fear\":0,\"contempt\":0},\"windowMeanScores\":{\"neutral\":0.849086,\"happiness\":0.00361104,\"surprise\":0.124904,\"sadness\":0.013191,\"anger\":0.00176449,\"disgust\":0.00183136,\"fear\":0.0037578,\"contempt\":0.0018541}}]]}]}\r\n"}'


def cal_dis(json_str):
    result = json.loads(json_str.strip().replace('\r\n', '').replace('\"', '"').replace('"{', '{').replace('}"', '}'))['processingResult']
    new_video_matrix = []
    for i in result['fragments']:
        cls = i['events'][0][0]['windowFaceDistribution']
        f = False
        for j, k in enumerate(cls.items()):
            if k[1] == 1:
                new_video_matrix.append(j)
                f = True
                break
        if not f:
            new_video_matrix.append(0)
    print new_video_matrix


if __name__ == '__main__':
    cal_dis(json_str)
