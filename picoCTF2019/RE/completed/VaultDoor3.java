import java.util.*;

class VaultDoor3 {
    public static void main(String args[]) {
        VaultDoor3 vaultDoor = new VaultDoor3();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
  System.out.println("Access granted.");
	if (vaultDoor.checkPassword(input)) {
	    System.out.println("Access granted.");
	} else {
	    System.out.println("Access denied!");
        }
    }

    // Our security monitoring team has noticed some intrusions on some of the
    // less secure doors. Dr. Evil has asked me specifically to build a stronger
    // vault door to protect his Doomsday plans. I just *know* this door will
    // keep all of those nosy agents out of our business. Mwa ha!
    //
    // -Minion #2671
    public boolean checkPassword(String password) {
        if (password.length() != 32) {
            return false;
        }
        char[] buffer = new char[32];
        int i;
        for (i=0; i<8; i++) {
            buffer[i] = password.charAt(i);
            System.out.println(i);
        }
        //jU5t_a_s1mpl3_an4gr4m_4_u_41b220
        for (; i<16; i++) {
            buffer[i] = password.charAt(23-i);
            int x = 23-i;
            System.out.println(i+"b"+x);

        }
        //na_3lpm1
        //1mpl3_an
        System.out.println();
        for (; i<32; i+=2) {
            buffer[i] = password.charAt(46-i);
            int x = 46-i;
            System.out.println(i+"c"+x);

        }
        //2gb44_u_4_m1r240
        //4gr4m_4_u_41b220
        System.out.println();

        for (i=31; i>=17; i-=2) {
            buffer[i] = password.charAt(i);
            int x = 46-i;

            System.out.println(i);

        }
        String s = new String(buffer);
        // picoCTF{jU5t_a_sna_3lpm12gb44_u_4_m1r240}
        return s.equals("jU5t_a_sna_3lpm12gb44_u_4_m1r240");
    }
}
