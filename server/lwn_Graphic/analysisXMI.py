import codecs

import untangle


def analysis(path, filename):
    # obj = untangle.parse('C:/Users/23789/Desktop/航天器方案设计.xml')
    obj = untangle.parse(path+filename)
    res = []
    d = {}
    for item in obj.xmi_XMI.uml_Model.packagedElement[0].packagedElement[0].packagedElement[0] \
            .region.subvertex:
        if item.get_attribute("name"):
            a = item.get_attribute("name")
            b = item.get_attribute("xmi:id")
            res.append(a)
            d[b] = a
        else:
            a = item.get_attribute("xmi:type").split(':')[1]
            b = item.get_attribute("xmi:id")
            res.append(a)
            d[b] = a

    for item in obj.xmi_XMI.uml_Model.packagedElement[0].packagedElement[0].packagedElement[0] \
            .region.subvertex[3].region.subvertex:
        if item.get_attribute("name"):
            a = item.get_attribute("name")
            b = item.get_attribute("xmi:id")
            res.append(a)
            d[b] = a
        else:
            a = item.get_attribute("xmi:type").split(':')[1]
            b = item.get_attribute("xmi:id")
            res.append(a)
            d[b] = a

    for item in obj.xmi_XMI.uml_Model.packagedElement[0].packagedElement[0].packagedElement[0] \
            .region.subvertex[3].region.subvertex[2].region.subvertex:
        if item.get_attribute("name"):
            a = item.get_attribute("name")
            b = item.get_attribute("xmi:id")
            res.append(a)
            d[b] = a
        else:
            a = item.get_attribute("xmi:type").split(':')[1]
            b = item.get_attribute("xmi:id")
            res.append(a)
            d[b] = a
    ra = []

    for item in obj.xmi_XMI.uml_Model.packagedElement[0].packagedElement[0].packagedElement[0].region.transition:
        a = item.get_attribute("source")
        b = item.get_attribute("target")
        ra.append((d[a], d[b]))

    for item in obj.xmi_XMI.uml_Model.packagedElement[0].packagedElement[0].packagedElement[0].region.subvertex[
        3].region.transition:
        a = item.get_attribute("source")
        b = item.get_attribute("target")
        ra.append((d[a], d[b]))

    for item in \
            obj.xmi_XMI.uml_Model.packagedElement[0].packagedElement[0].packagedElement[0].region.subvertex[
                3].region.subvertex[
                2].region.transition:
        a = item.get_attribute("source")
        b = item.get_attribute("target")
        ra.append((d[a], d[b]))

    wf = codecs.open(path+"result2.txt", 'w', encoding="utf-8")
    for key in range(len(res)):
        wf.write("State:\n\tlabel=S" + str(key) + '\n\t' + "name=" + res[key] + '\n')

    zd = {}
    key = 0
    for name in res:
        zd[name] = 'S' + str(key)
        key += 1
    for key in range(len(ra)):
        if key == len(ra) - 1:
            wf.write("Transition:\n\t\tname=T" + str(key) + '\n\t\tsrc=' + zd[ra[key][0]] + '\n\t\ttgt=' + zd[
                ra[key][0]] + '\n\t\t' + 'event=' + '\n\t\t' + 'condition=' + '\n\t\t' + 'action=')
        else:
            wf.write("Transition:\n\t\tname=T" + str(key) + '\n\t\tsrc=' + zd[ra[key][0]] \
                     + '\n\t\ttgt=' + zd[
                         ra[key][1]] + '\n\t\t' + 'event=' + '\n\t\t' + 'condition=' + '\n\t\t' + 'action=' + '\n')
    wf.close()
    # print(res)
    # print(ra)
