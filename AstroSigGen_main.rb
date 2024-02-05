require 'socket'

# ---------------------------------------------------
# Class Astro SG
# ---------------------------------------------------
class AstroSG
    def initialize(address, port)
        @udp        = UDPSocket.open()
        @sockaddr   = Socket.pack_sockaddr_in(port, address)
		printf("initialize \n")
    end

    def connect
        msg = [0x05].pack("C")
        @udp.send(msg, 0, @sockaddr)
        sleep(1)
		puts "msg = #{msg}"
		printf("connect \n")
		
    end

    def disconnect
        msg = [0x04].pack("C")
		puts "msg = #{msg}"
        @udp.send(msg, 0, @sockaddr)
        @udp.close
		printf("disconnect \n")
    end

    def setProgNum(progNum)
       if 4 == progNum.split(//).size then
          param = [ ("3"+progNum[0]).hex, ("3"+progNum[1]).hex, ("3"+progNum[2]).hex, ("3"+progNum[3]).hex]
          msg = [0x02, 0xfd, 0x24, 0x20, param[0], param[1], param[2], param[3], 0x2c, 0x31, 0x03].pack("C*")
          @udp.send(msg, 0, @sockaddr)
		  puts "msg = #{msg}"
       elsif 3 == progNum.split(//).size then
          param = [ ("3"+"0").hex, ("3"+progNum[0]).hex, ("3"+progNum[1]).hex, ("3"+progNum[2]).hex]
          msg = [0x02, 0xfd, 0x24, 0x20, param[0], param[1], param[2], param[3], 0x2c, 0x31, 0x03].pack("C*")
          @udp.send(msg, 0, @sockaddr)
       else
          printf("Error!! Program Number %s is wrong \n", progNum)
          exit 2
       end
    end
end

# Astro SG
SG_ADDR  = "192.168.122.56"
SG_PORT  = 8000

astroSG = AstroSG.new(SG_ADDR, SG_PORT)
astroSG.connect
astroSG.setProgNum("1005")

sleep 10

puts "Input to exit"
input = gets
if(input == "e") then
astroSG.disconnect
end