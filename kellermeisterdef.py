import numpy as np # for structured arrays
from xml.dom import minidom
import codecs

codec="utf-8"
codec="latin1"

xmldoc = minidom.parse('storages.xml')
storage = xmldoc.getElementsByTagName('storage')

def getEntry(storage,key):
        alist=storage.getElementsByTagName(key)
        ret = ""
        for a in alist:
            ret = a.childNodes[0].nodeValue
        return ret.encode(codec, 'ignore')

# https://jakevdp.github.io/PythonDataScienceHandbook/02.09-structured-data-numpy.html
#
# Here 'U10' translates to "Unicode string of maximum length 10," 'i4'
# translates to "4-byte (i.e., 32 bit) integer," and 'f8' translates to "8-byte
# (i.e., 64 bit) float." We'll discuss other options for these type codes in
# the following section.
# 'b'	Byte	np.dtype('b')
# 'i'	Signed integer	np.dtype('i4') == np.int32
# 'u'	Unsigned integer	np.dtype('u1') == np.uint8
# 'f'	Floating point	np.dtype('f8') == np.int64
# 'c'	Complex floating point	np.dtype('c16') == np.complex128
# 'S', 'a'	String	np.dtype('S5')
# 'U'	Unicode string	np.dtype('U') == np.str_
# 'V'	Raw data (void)	np.dtype('V') == np.void

tdata = np.dtype([
    ('uuid' , 'U20'),
    ('vintage' , 'U20'),
    ('label' , 'U60'),
    ('labelBack' , 'U60'),
    ('country' , 'U20'),
    ('region' , 'U20'),
    ('appellation' , 'U20'),
    ('type' , 'U20'),
    ('volume' , 'U20'),
    ('varietal' , 'U20'),
    ('location' , 'U20'),
    ('initialStorageCount' , 'i4'),
    ('currentStorageCount' , 'i4'),
    ('price' , 'f8'),
    ('alcoholStrength' , 'f8'),
    ('sugar' , 'f8'),
    ('acidity' , 'f8'),
    ('rating' , 'U20'),
    ('bestAge' , 'i4'),
    ('minAge' , 'i4'),
    ('maxAge' , 'i4'),
    ('scancode' , 'U20'),
    ('scancodeFormat' , 'U20'),
    ('favourite' , 'i4'),
    ('note' , 'U60'),
    ('deleted' , 'i4')
])

odata = np.zeros(storage.length+1, 
        dtype={'names':('vintage', 'varietal', 'label', 'cnt', 'locs', 'type', 'price'),
                          'formats':('U20', 'U20', 'U60', 'i4', 'U20', 'U20', 'f8')
                         })
data = np.zeros(storage.length+1, tdata)
dcnt = 0

## unfinished work...

def decode(s) : 
    global dcnt
    vint  = getEntry(s,'vintage').decode(codec)
    val   = getEntry(s,'varietal').decode(codec)
    lbl   = getEntry(s,'label').decode(codec)
    cnt   = getEntry(s,'currentStorageCount').decode(codec)
    locs  = getEntry(s,'location').decode(codec)
    wtype = getEntry(s,'type').decode(codec)  # rot / weiß
    price = float(getEntry(s,'price'))
    D = data[dcnt]
    D['vintage'] = vint
    D['varietal'] = val
    D['label'] = lbl
    D['location'] = locs
    D['currentStorageCount'] = cnt
    D['type'] = wtype
    D['price'] = price
    dcnt = dcnt+1
    return D

#     <uuid>0862e048-0567-4812-baaa-9e3e120bb353</uuid>
#     <vintage>2013</vintage>
#     <label>7391db12-c281-44e1-ae7d-3e0d925daad6.jpg</label>
#     <labelBack>afdf8ee0-9bba-4a1f-9d0b-e1a9ebcda394.jpg</labelBack>
#     <country>Frankreich</country>
#     <region>Burgund</region>
#     <appellation>Côte de Nuits Villages</appellation>
#     <type>Rotwein</type>
#     <volume>0.699999988079071</volume>
#     <varietal>Pinot Noir</varietal>
#     <location>J05</location>
#     <initialStorageCount>1</initialStorageCount>
#     <currentStorageCount>0</currentStorageCount>
#     <price currency="EUR">0.0</price>
#     <alcoholStrength>-1.0</alcoholStrength>
#     <sugar>-1.0</sugar>
#     <acidity>-1.0</acidity>
#     <rating>0.0</rating>
#     <bestAge>0</bestAge>
#     <minAge>0</minAge>
#     <maxAge>6</maxAge>
#     <scancode>3463640090751</scancode>
#     <scancodeFormat>EAN_13</scancodeFormat>
#     <favourite>0</favourite>
#     <deleted>false</deleted>
