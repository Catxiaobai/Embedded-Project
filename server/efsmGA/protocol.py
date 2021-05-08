class protocol(object):
    def __init__(self):
        self.frame_head=1431655765
        self.message_length=0
        self.message_ID=513
        self.message_send_time=0
        self.message_send_sequence_number=1
        self.start_or_stop=1
        self.reservations1=0
        self.reservations2=0
        self.type_of_data_collected=1
        self.reservations3=0
        self.frame_end=2863311530

    def read(self):
        print "This Message:",self.frame_head,",",self.message_length,",",self.message_ID,",",self.message_send_time,",",self.message_send_sequence_number,",",self.start_or_stop,",",self.reservations1,",",self.reservations2,",",self.type_of_data_collected,",",self.reservations3,",",self.frame_end
        return self.frame_head,self.message_length,self.message_ID,self.message_send_time,self.message_send_sequence_number,self.start_or_stop,self.reservations1,self.reservations2,self.type_of_data_collected,self.reservations3,self.frame_end

    def check(self):
        Error=""
        flag=True
        if self.frame_head!=1431655765 or self.frame_head<0 or self.frame_head> 2**32-1:
            Error="frame_head"
            flag=False
        if self.message_length<0 or self.message_length> 2**32-1:
            Error = "message_length"
            flag = False
        if self.message_ID != 513 or self.message_ID<0 or self.message_ID> 2**16-1:
            Error = "message_ID"
            flag = False
        if self.message_send_time<0 or self.message_send_time> 2**64-1:
            Error = "message_send_time"
            flag = False
        if self.message_send_sequence_number<0 or self.message_send_sequence_number>2**16-1:
            Error = "message_send_sequence_number"
            flag = False
        if self.start_or_stop not in [0,1] or self.start_or_stop < 0 or self.start_or_stop > 2**8-1:
            Error = "start_or_stop"
            flag = False
        if self.reservations1< 0 or self.reservations1 > 2**16-1:
            Error = "reservations1"
            flag = False
        if self.reservations2 < 0 or self.reservations2 > 2**16-1:
            Error = "reservations2"
            flag = False
        if self.type_of_data_collected not in [1,2,3,4] or self.type_of_data_collected < 0 or self.type_of_data_collected > 2**8-1:
            Error = "type_of_data_collected"
            flag = False
        if self.reservations3 < 0 or self.reservations3  > 2**16-1:
            Error = "reservations3"
            flag = False
        if self.frame_end != 2863311530 or self.frame_end<0 or self.frame_end> 2**32-1:
            Error = "frame_end"
            flag = False
        return flag,Error
    def set_message_length(self,temp):
        self.message_length = temp

    def set_message_ID(self,temp):
        self.message_ID = temp

    def set_message_send_time(self,temp):
        self.message_send_time = temp

    def set_message_send_sequence_number(self,temp):
        self.message_send_sequence_number = temp

    def set_start_or_stop(self,temp):
        self.start_or_stop = temp

    def set_reservations1(self,temp):
        self.reservations1 = temp

    def set_reservations2(self,temp):
        self.reservations2 = temp

    def set_type_of_data_collected(self,temp):
        self.type_of_data_collected = temp

    def set_reservations3(self,temp):
        self.reservations3 = temp

    def set_ALL(self,temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9):
        self.message_length = temp1
        self.message_ID = temp2
        self.message_send_time = temp3
        self.message_send_sequence_number = temp4
        self.start_or_stop = temp5
        self.reservations1 = temp6
        self.reservations2 = temp7
        self.type_of_data_collected = temp8
        self.reservations3 = temp9
    def clear(self):
        self.frame_head = 1431655765
        self.message_length = 0
        self.message_ID = 513
        self.message_send_time = 0
        self.message_send_sequence_number = 1
        self.start_or_stop = 1
        self.reservations1 = 0
        self.reservations2 = 0
        self.type_of_data_collected = 1
        self.reservations3 = 0
        self.frame_end = 2863311530
if __name__ == '__main__':
    protocol1=protocol()
    protocol1.read()
    protocol1.set_ALL(1,513,1,1,1,1,1,1,1)
    print protocol1.check()
    protocol1.read()
