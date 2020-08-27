#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: predict_model.py
@time: 2020/08/27
"""
from get_train_factors import integrate_features
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn import tree
def correlation_analysis(data):#对dataframe里的各个参数做相关性分析

    corr = data.corr(method='pearson')  # 使用皮尔逊系数计算列与列的相关性
    # corr=data.corr(method='kendall')# 肯德尔秩相关系数
    # corr=data.corr(method='spearman')# 斯皮尔曼秩相关系数
    # print(corr)
    fig, ax = plt.subplots(figsize=(10, 10))  # 分辨率1200×1000
    cmap = sns.diverging_palette(220, 10,
                                 as_cmap=True)  # 在两种HUSL颜色之间制作不同的调色板。图的正负色彩范围为220、10，结果为真则返回matplotlib的colormap对象
    fig = sns.heatmap(
        corr,  # 使用Pandas DataFrame数据，索引/列信息用于标记列和行
        cmap=cmap,  # 数据值到颜色空间的映射
        square=True,  # 每个单元格都是正方形
        cbar_kws={'shrink': .9},  # `fig.colorbar`的关键字参数
        ax=ax,  # 绘制图的轴
        annot=True,  # 在单元格中标注数据值
        annot_kws={'fontsize': 8})  # 热图，将矩形数据绘制为颜色编码矩阵

    plt.ylim(0, len(corr))  # 解决y轴文字错乱
    plt.gcf().subplots_adjust(left=0.2, bottom=0.2)  # 解决show图时底部显示不全
    plt.tight_layout()  # 解决坐标文字显示不全###
    plt.savefig('stock_{}/相关性分析.png'.format(ts_code))
    plt.show()

def decision_tree_model(data):
    # feature_cols = ['VAL_LNMV', 'RISK_VARIANCE20', 'WEST_NETPROFIT_FY1_1M', 'TECH_REVS5', 'TECH_TURNOVERRATE20',
    #                 'TECH_BEARPOWER', 'TECH_CYF', 'KLINE_TYPE','WEIGHT-BY-BOLL', 'MTR/ATR'
    #                 ]
    feature_cols = ['KLINE_TYPE','WEIGHT-BY-BOLL', 'MTR/ATR']
    # 机器学习建模
    X = data[feature_cols]
    y = data['LABEL']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=0,
                                                        stratify=y)  # 按label比例划分训练集数据集

    # std=StandardScaler()
    # X_train=std.fit_transform(X_train)
    # X_test=std.fit_transform(X_test)#数据归一化

    clf = DecisionTreeClassifier(criterion='entropy', max_depth=3, class_weight='balanced')
    clf.fit(X_train, y_train)
    y_pred_test = clf.predict(X_test)
    y_pred_train = clf.predict(X_train)
    print("\n\n---Decision tree---")
    print(classification_report(y_test, y_pred_test))

    print("Train Accuracy:", metrics.accuracy_score(y_train, y_pred_train))
    print("Test Accuracy:", metrics.accuracy_score(y_test, y_pred_test))

    cm = confusion_matrix(y_test, y_pred_test)

    # 输出混淆矩阵
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, cmap='Blues')

    plt.ylim(0, 3)
    plt.xlabel('Predicted lables')
    plt.ylabel('True lables')
    plt.show()

    # 决策树模型的可视化
    tree.plot_tree(clf)
    # fn = ['VAL_LNMV', 'RISK_VARIANCE20', 'WEST_NETPROFIT_FY1_1M', 'TECH_REVS5', 'TECH_TURNOVERRATE20',
    #       'TECH_BEARPOWER', 'TECH_CYF', 'WEIGHT-BY-BOLL', 'MTR/ATR']
    fn = ['KLINE_TYPE','WEIGHT-BY-BOLL', 'MTR/ATR']
    cn = ['0', '1', '2']
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 8), dpi=300)
    tree.plot_tree(clf,
                   feature_names=fn,
                   class_names=cn,
                   filled=True)
    fig.savefig('stock_{}/stock_Decisiontree.png'.format(ts_code))

if __name__ == "__main__":
    ts_code = '300725.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2018-01-01'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    data=integrate_features(ts_code, start_date, end_date)
    correlation_analysis(data)
    decision_tree_model(data)
