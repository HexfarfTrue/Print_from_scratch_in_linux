#![no_std]
#![no_main]

use core::panic::PanicInfo;

extern "C" {
    fn print();
    fn exit_program(code: i32) -> !;
}

#[no_mangle]
pub extern "C" fn _start() -> ! {
    unsafe {
        print();
        exit_program(0);
    } 
}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
   
    unsafe {
        exit_program(1);
    }
}
