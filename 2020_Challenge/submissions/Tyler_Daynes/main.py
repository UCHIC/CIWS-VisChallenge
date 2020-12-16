if __name__ == '__main__':
    import pandas as pd
    from matplotlib import pyplot as plt
    import squarify as sq
    import dataimport  # module that collects data from the csv file

    color_list = ['#0082bb',
                  '#248dc6',
                  '#3797d1',
                  '#47a2dc',
                  '#56ade8',
                  '#64b8f3']

    color_list1 = ['#0082bb',
                   '#298fc9',
                   '#409dd7',
                   '#53aae5',
                   '#64b8f3']

    # Color scale from https://learnui.design/tools/data-color-picker.html#single

    # Volume Plot
    dictionary = dict(zip(dataimport.categories, dataimport.V_sum))
    df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Value'])
    df = df.sort_values(by=['Value'], ascending=False)
    df['Color'] = color_list

    plt.figure(figsize=(7.5, 5.5))
    plt.pie(df.Value, labels=df.index, autopct='%1.1f%%', startangle=18,
            colors=color_list, pctdistance=0.85)
    circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(circle)
    text = f'Total Volume: {round(df.Value.sum(), 2):,} Gallons'
    plt.text(0, 0, text, ha='center', wrap=True)
    plt.axis('equal')
    plt.title('Total Volume Used')

    plt.tight_layout()
    plt.savefig('./Plots/TotalVolume.png')
    plt.show()

    # Volume plot without Irrigation
    df = df.drop(labels='Irrigation')
    df.Color = color_list1

    plt.figure(figsize=(7.5, 5.5))
    plt.pie(df.Value, labels=df.index, autopct='%1.1f%%', startangle=60,
            colors=color_list1, pctdistance=0.85)
    circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(circle)
    text = f'Total Volume {round(df.Value.sum(), 2):,} Gallons'
    plt.text(0, 0, text, ha='center', wrap=True)
    plt.axis('equal')
    plt.title('Total Volume Used Excluding Irrigation')

    plt.tight_layout()
    plt.savefig('./Plots/TotalVolumeIrr.png')
    plt.show()

    # Duration plot
    dictionary = dict(zip(dataimport.categories, dataimport.D_sum))
    df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Value'])
    df = df.sort_values(by=['Value'], ascending=False)
    df['Color'] = color_list

    plt.figure(figsize=(7.5, 5.5))
    plt.pie(df.Value, labels=df.index, autopct='%1.1f%%', startangle=60,
            colors=color_list, pctdistance=0.85)
    circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(circle)
    text = f'Total Operating Time: {round(df.Value.sum() / 60, 2):,} Hours'
    plt.text(0, 0, text, ha='center', wrap=True)
    plt.axis('equal')
    plt.title('Equipment Operating Time')

    plt.tight_layout()
    plt.savefig('./Plots/Duration.png')
    plt.show()

    # Duration without irrigation plot
    df = df.drop(labels='Irrigation')
    df.Color = color_list1

    plt.figure(figsize=(7.5, 5.5))
    plt.pie(df.Value, labels=df.index, autopct='%1.1f%%', startangle=60,
            colors=color_list, pctdistance=0.85)
    circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(circle)
    text = f'Total Operating Time: {round(df.Value.sum() / 60, 2):,} Hours'
    plt.text(0, 0, text, ha='center', wrap=True)
    plt.axis('equal')
    plt.title('Equipment Operating Time Excluding Irrigation')

    plt.tight_layout()
    plt.savefig('./Plots/DurationIrr.png')
    plt.show()

    # Mean volume plot
    dictionary = dict(zip(dataimport.categories, dataimport.V_mean))
    df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Value'])
    df = df.sort_values(by=['Value'], ascending=False)
    df = df.drop(labels='Irrigation')
    df['Color'] = color_list1
    # labels = list(zip(df.index, df.Value.round(decimals=2)))
    labels = ['%s\n %.1f Gallons' % label for label in zip(df.index, df.Value.round(decimals=1))]

    plt.figure(figsize=(7.5, 5.5))
    sq.plot(sizes=df.Value, label=labels, color=color_list, pad=True)
    plt.axis('off')
    plt.title('Average Volume Used in Each Occurrence')

    plt.tight_layout()
    plt.savefig('./Plots/VolumeAVG.png')
    plt.show()
