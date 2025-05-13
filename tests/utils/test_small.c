typedef unsigned int size_t;
typedef signed char int8_t;
typedef short int int16_t;
typedef int int32_t;
typedef long long int int64_t;
typedef unsigned char uint8_t;
typedef unsigned short int uint16_t;
typedef unsigned int uint32_t;
typedef unsigned long long int uint64_t;
int printf (const char *, ...);
void __assert_fail (const char *__assertion, const char *__file, unsigned int __line, const char *__function);

static int8_t
(safe_unary_minus_func_int8_t_s)(int8_t si )
{

  return






    -si;
}

static int8_t
(safe_add_func_int8_t_s_s)(int8_t si1, int8_t si2 )
{

  return






    (si1 + si2);
}

static int8_t
(safe_sub_func_int8_t_s_s)(int8_t si1, int8_t si2 )
{

  return






    (si1 - si2);
}



static int8_t
(safe_mod_func_int8_t_s_s)(int8_t si1, int8_t si2 )
{

  return

    ((si2 == 0) || ((si1 == (-128)) && (si2 == (-1)))) ?
    ((si1)) :

    (si1 % si2);
}

static int8_t
(safe_div_func_int8_t_s_s)(int8_t si1, int8_t si2 )
{

  return

    ((si2 == 0) || ((si1 == (-128)) && (si2 == (-1)))) ?
    ((si1)) :

    (si1 / si2);
}

static int8_t
(safe_lshift_func_int8_t_s_s)(int8_t left, int right )
{

  return

    ((left < 0) || (((int)right) < 0) || (((int)right) >= 32) || (left > ((127) >> ((int)right)))) ?
    ((left)) :

    (left << ((int)right));
}

static int8_t
(safe_lshift_func_int8_t_s_u)(int8_t left, unsigned int right )
{

  return

    ((left < 0) || (((unsigned int)right) >= 32) || (left > ((127) >> ((unsigned int)right)))) ?
    ((left)) :

    (left << ((unsigned int)right));
}

static int8_t
(safe_rshift_func_int8_t_s_s)(int8_t left, int right )
{

  return

    ((left < 0) || (((int)right) < 0) || (((int)right) >= 32))?
    ((left)) :

    (left >> ((int)right));
}

static int8_t
(safe_rshift_func_int8_t_s_u)(int8_t left, unsigned int right )
{

  return

    ((left < 0) || (((unsigned int)right) >= 32)) ?
    ((left)) :

    (left >> ((unsigned int)right));
}



static int16_t
(safe_unary_minus_func_int16_t_s)(int16_t si )
{

  return






    -si;
}

static int16_t
(safe_add_func_int16_t_s_s)(int16_t si1, int16_t si2 )
{

  return






    (si1 + si2);
}

static int16_t
(safe_sub_func_int16_t_s_s)(int16_t si1, int16_t si2 )
{

  return






    (si1 - si2);
}

static int16_t
(safe_mul_func_int16_t_s_s)(int16_t si1, int16_t si2 )
{

  return






    si1 * si2;
}

static int16_t
(safe_mod_func_int16_t_s_s)(int16_t si1, int16_t si2 )
{

  return

    ((si2 == 0) || ((si1 == (-32767-1)) && (si2 == (-1)))) ?
    ((si1)) :

    (si1 % si2);
}



static int16_t
(safe_lshift_func_int16_t_s_s)(int16_t left, int right )
{

  return

    ((left < 0) || (((int)right) < 0) || (((int)right) >= 32) || (left > ((32767) >> ((int)right)))) ?
    ((left)) :

    (left << ((int)right));
}

static int16_t
(safe_lshift_func_int16_t_s_u)(int16_t left, unsigned int right )
{

  return

    ((left < 0) || (((unsigned int)right) >= 32) || (left > ((32767) >> ((unsigned int)right)))) ?
    ((left)) :

    (left << ((unsigned int)right));
}

static int16_t
(safe_rshift_func_int16_t_s_s)(int16_t left, int right )
{

  return

    ((left < 0) || (((int)right) < 0) || (((int)right) >= 32))?
    ((left)) :

    (left >> ((int)right));
}

static int16_t
(safe_rshift_func_int16_t_s_u)(int16_t left, unsigned int right )
{

  return

    ((left < 0) || (((unsigned int)right) >= 32)) ?
    ((left)) :

    (left >> ((unsigned int)right));
}



static int32_t
(safe_unary_minus_func_int32_t_s)(int32_t si )
{

  return


    (si==(-2147483647-1)) ?
    ((si)) :


    -si;
}

static int32_t
(safe_add_func_int32_t_s_s)(int32_t si1, int32_t si2 )
{

  return


    (((si1>0) && (si2>0) && (si1 > ((2147483647)-si2))) || ((si1<0) && (si2<0) && (si1 < ((-2147483647-1)-si2)))) ?
    ((si1)) :


    (si1 + si2);
}

static int32_t
(safe_sub_func_int32_t_s_s)(int32_t si1, int32_t si2 )
{

  return


    (((si1^si2) & (((si1 ^ ((si1^si2) & (~(2147483647))))-si2)^si2)) < 0) ?
    ((si1)) :


    (si1 - si2);
}

static int32_t
(safe_mul_func_int32_t_s_s)(int32_t si1, int32_t si2 )
{

  return


    (((si1 > 0) && (si2 > 0) && (si1 > ((2147483647) / si2))) || ((si1 > 0) && (si2 <= 0) && (si2 < ((-2147483647-1) / si1))) || ((si1 <= 0) && (si2 > 0) && (si1 < ((-2147483647-1) / si2))) || ((si1 <= 0) && (si2 <= 0) && (si1 != 0) && (si2 < ((2147483647) / si1)))) ?
    ((si1)) :


    si1 * si2;
}

static int32_t
(safe_mod_func_int32_t_s_s)(int32_t si1, int32_t si2 )
{

  return

    ((si2 == 0) || ((si1 == (-2147483647-1)) && (si2 == (-1)))) ?
    ((si1)) :

    (si1 % si2);
}










static uint8_t
(safe_unary_minus_func_uint8_t_u)(uint8_t ui )
{

  return -ui;
}

static uint8_t
(safe_add_func_uint8_t_u_u)(uint8_t ui1, uint8_t ui2 )
{

  return ui1 + ui2;
}

static uint8_t
(safe_sub_func_uint8_t_u_u)(uint8_t ui1, uint8_t ui2 )
{

  return ui1 - ui2;
}

static uint8_t
(safe_mul_func_uint8_t_u_u)(uint8_t ui1, uint8_t ui2 )
{

  return ((unsigned int)ui1) * ((unsigned int)ui2);
}

static uint8_t
(safe_mod_func_uint8_t_u_u)(uint8_t ui1, uint8_t ui2 )
{

  return

    (ui2 == 0) ?
    ((ui1)) :

    (ui1 % ui2);
}



static uint8_t
(safe_lshift_func_uint8_t_u_s)(uint8_t left, int right )
{

  return

    ((((int)right) < 0) || (((int)right) >= 32) || (left > ((255) >> ((int)right)))) ?
    ((left)) :

    (left << ((int)right));
}

static uint8_t
(safe_lshift_func_uint8_t_u_u)(uint8_t left, unsigned int right )
{

  return

    ((((unsigned int)right) >= 32) || (left > ((255) >> ((unsigned int)right)))) ?
    ((left)) :

    (left << ((unsigned int)right));
}

static uint8_t
(safe_rshift_func_uint8_t_u_s)(uint8_t left, int right )
{

  return

    ((((int)right) < 0) || (((int)right) >= 32)) ?
    ((left)) :

    (left >> ((int)right));
}







static uint16_t
(safe_add_func_uint16_t_u_u)(uint16_t ui1, uint16_t ui2 )
{

  return ui1 + ui2;
}

static uint16_t
(safe_sub_func_uint16_t_u_u)(uint16_t ui1, uint16_t ui2 )
{

  return ui1 - ui2;
}

static uint16_t
(safe_mul_func_uint16_t_u_u)(uint16_t ui1, uint16_t ui2 )
{

  return ((unsigned int)ui1) * ((unsigned int)ui2);
}

static uint16_t
(safe_mod_func_uint16_t_u_u)(uint16_t ui1, uint16_t ui2 )
{

  return

    (ui2 == 0) ?
    ((ui1)) :

    (ui1 % ui2);
}

static uint16_t
(safe_div_func_uint16_t_u_u)(uint16_t ui1, uint16_t ui2 )
{

  return

    (ui2 == 0) ?
    ((ui1)) :

    (ui1 / ui2);
}

static uint16_t
(safe_lshift_func_uint16_t_u_s)(uint16_t left, int right )
{

  return

    ((((int)right) < 0) || (((int)right) >= 32) || (left > ((65535) >> ((int)right)))) ?
    ((left)) :

    (left << ((int)right));
}



static uint16_t
(safe_rshift_func_uint16_t_u_s)(uint16_t left, int right )
{

  return

    ((((int)right) < 0) || (((int)right) >= 32)) ?
    ((left)) :

    (left >> ((int)right));
}

static uint16_t
(safe_rshift_func_uint16_t_u_u)(uint16_t left, unsigned int right )
{

  return

    (((unsigned int)right) >= 32) ?
    ((left)) :

    (left >> ((unsigned int)right));
}



static uint32_t
(safe_unary_minus_func_uint32_t_u)(uint32_t ui )
{

  return -ui;
}

static uint32_t
(safe_add_func_uint32_t_u_u)(uint32_t ui1, uint32_t ui2 )
{

  return ui1 + ui2;
}

static uint32_t
(safe_sub_func_uint32_t_u_u)(uint32_t ui1, uint32_t ui2 )
{

  return ui1 - ui2;
}

static uint32_t
(safe_mul_func_uint32_t_u_u)(uint32_t ui1, uint32_t ui2 )
{

  return ((unsigned int)ui1) * ((unsigned int)ui2);
}

static uint32_t
(safe_mod_func_uint32_t_u_u)(uint32_t ui1, uint32_t ui2 )
{

  return

    (ui2 == 0) ?
    ((ui1)) :

    (ui1 % ui2);
}

static uint32_t
(safe_div_func_uint32_t_u_u)(uint32_t ui1, uint32_t ui2 )
{

  return

    (ui2 == 0) ?
    ((ui1)) :

    (ui1 / ui2);
}










static uint32_t crc32_tab[256];
static uint32_t crc32_context = 0xFFFFFFFFUL;



static void
crc32_byte (uint8_t b) {
 crc32_context =
  ((crc32_context >> 8) & 0x00FFFFFF) ^
  crc32_tab[(crc32_context ^ b) & 0xFF];
}


static void
crc32_8bytes (uint32_t val)
{
 crc32_byte ((val>>0) & 0xff);
 crc32_byte ((val>>8) & 0xff);
 crc32_byte ((val>>16) & 0xff);
 crc32_byte ((val>>24) & 0xff);
}

static void
transparent_crc (uint32_t val, char* vname, int flag)
{
 crc32_8bytes(val);
 if (flag) {
    printf("...checksum after hashing %s : %X\n", vname, crc32_context ^ 0xFFFFFFFFU);
 }
}



static long __undefined;


struct S0 {
   int8_t f0;
   int8_t f1;
   uint32_t f2;
   int32_t f3;
   uint16_t f4;
};


static int32_t g_3 = 0x9BA095A9L;
static int32_t g_4[10][4][2] = {{{0xD4A0D461L,0xFC3A065CL},{1L,0xD4A0D461L},{0x8DC5336DL,0x8DC5336DL},{0x8DC5336DL,0xD4A0D461L}},{{1L,0xFC3A065CL},{0xD4A0D461L,0xFC3A065CL},{1L,0xD4A0D461L},{0x8DC5336DL,0x8DC5336DL}},{{0x8DC5336DL,0xD4A0D461L},{1L,0xFC3A065CL},{0xD4A0D461L,0xFC3A065CL},{1L,0xD4A0D461L}},{{0x8DC5336DL,0x8DC5336DL},{0x8DC5336DL,0xD4A0D461L},{1L,0xFC3A065CL},{0xD4A0D461L,0xFC3A065CL}},{{1L,0xD4A0D461L},{0x8DC5336DL,0x8DC5336DL},{0x8DC5336DL,0xD4A0D461L},{1L,0xFC3A065CL}},{{0xD4A0D461L,0xFC3A065CL},{1L,0xD4A0D461L},{0x8DC5336DL,0x8DC5336DL},{0xD4A0D461L,1L}},{{0xC8F0D071L,0x8DC5336DL},{1L,0x8DC5336DL},{0xC8F0D071L,1L},{0xD4A0D461L,0xD4A0D461L}},{{0xD4A0D461L,1L},{0xC8F0D071L,0x8DC5336DL},{1L,0x8DC5336DL},{0xC8F0D071L,1L}},{{0xD4A0D461L,0xD4A0D461L},{0xD4A0D461L,1L},{0xC8F0D071L,0x8DC5336DL},{1L,0x8DC5336DL}},{{0xC8F0D071L,1L},{0xD4A0D461L,0xD4A0D461L},{0xD4A0D461L,1L},{0xC8F0D071L,0x8DC5336DL}}};
static int32_t g_5[3] = {0xB2C41AC3L,0xB2C41AC3L,0xB2C41AC3L};
static uint8_t g_22 = 0x4CL;
static uint32_t g_23[3] = {0x69C1477AL,0x69C1477AL,0x69C1477AL};
static int8_t g_26 = 4L;
static uint16_t g_27 = 65532UL;
static uint16_t g_32 = 0xB7A2L;
static uint8_t g_55[9][8] = {{252UL,255UL,0x79L,3UL,0x17L,3UL,0UL,255UL},{249UL,0UL,0xE3L,3UL,251UL,255UL,0UL,251UL},{0xD5L,251UL,247UL,0xD5L,249UL,255UL,0x5BL,252UL},{0UL,0xD5L,255UL,0UL,255UL,0xD5L,0UL,0x17L},{0x1CL,255UL,255UL,0x8AL,0x49L,4UL,0x8AL,0UL},{247UL,251UL,0xD5L,0x7EL,0x49L,0x5BL,0UL,0UL},{0x1CL,0x79L,0x7EL,0UL,255UL,3UL,251UL,0x5BL},{0UL,0x49L,255UL,249UL,249UL,255UL,0x49L,0UL},{0xD5L,3UL,0UL,0x17L,251UL,255UL,247UL,0x8AL}};
static int32_t g_57 = 0xEB039226L;
static int32_t g_58 = 4L;
static uint32_t g_59[9] = {0x18880ABBL,0x18880ABBL,0x18880ABBL,0x18880ABBL,0x18880ABBL,0x18880ABBL,0x18880ABBL,0x18880ABBL,0x18880ABBL};
static uint32_t g_69 = 0x797CFCBFL;
static int32_t g_80 = 0xD47B9DA0L;
static uint32_t g_81[4] = {0xFACDC9FFL,0xFACDC9FFL,0xFACDC9FFL,0xFACDC9FFL};
static struct S0 g_152[2] = {{0x6EL,1L,0UL,0x4AB730D5L,0UL},{0x6EL,1L,0UL,0x4AB730D5L,0UL}};
static uint16_t g_203[3] = {0x582DL,0x582DL,0x582DL};
static int32_t g_214 = (-2L);
static uint32_t g_231 = 4294967286UL;
static int16_t g_234 = 0L;
static int16_t g_277 = 1L;
static struct S0 g_283 = {0xB0L,-1L,0xF2B8033DL,0x5451DF1BL,0x022DL};
static uint32_t g_407 = 0x57A78FE8L;
static int32_t g_410 = 0x38F403BAL;
static int32_t g_465 = 0x5F3E33FAL;
static uint32_t g_466 = 0UL;
static int16_t g_551 = (-1L);
static int32_t g_616[5] = {0x79C30704L,0x79C30704L,0x79C30704L,0x79C30704L,0x79C30704L};
static int32_t g_621[2][9][5] = {{{(-10L),1L,0xD5EF2F06L,1L,(-10L)},{1L,1L,8L,(-10L),8L},{8L,8L,0xD5EF2F06L,(-10L),0x1E4228D9L},{1L,1L,1L,1L,8L},{1L,(-10L),(-4L),(-4L),(-10L)},{8L,1L,(-4L),0xD5EF2F06L,0xD5EF2F06L},{1L,8L,1L,(-4L),0xD5EF2F06L},{(-10L),1L,0xD5EF2F06L,1L,(-10L)},{1L,1L,8L,(-10L),8L}},{{8L,8L,0xD5EF2F06L,(-10L),0x1E4228D9L},{1L,1L,1L,1L,8L},{1L,(-4L),0xD5EF2F06L,0xD5EF2F06L,(-4L)},{0x1E4228D9L,(-10L),0xD5EF2F06L,8L,8L},{(-10L),0x1E4228D9L,(-10L),0xD5EF2F06L,8L},{(-4L),1L,8L,1L,(-4L)},{(-10L),1L,0x1E4228D9L,(-4L),0x1E4228D9L},{0x1E4228D9L,0x1E4228D9L,8L,(-4L),1L},{1L,(-10L),(-10L),1L,0x1E4228D9L}}};
static int32_t g_973 = 0x44345857L;
static uint32_t g_976 = 4294967294UL;
static int16_t g_1185 = (-1L);
static int32_t g_1356 = 0x0FA767BCL;
static uint16_t g_1477 = 0xBAB5L;
static uint32_t g_1570 = 0x6920269FL;
static uint32_t g_1707 = 5UL;
static uint8_t g_1917 = 0x44L;
static int32_t g_2181 = 9L;
static uint32_t g_2432 = 4294967293UL;



static struct S0 func_1(void);
static uint16_t func_13(int8_t p_14, int32_t p_15, uint32_t p_16);
static int32_t func_17(int32_t p_18, uint16_t p_19, uint8_t p_20, uint32_t p_21);
static uint8_t func_72(struct S0 p_73, uint32_t p_74, int32_t p_75);
static struct S0 func_76(uint32_t p_77, int16_t p_78, uint8_t p_79);
static uint8_t func_99(uint32_t p_100);
static uint32_t func_105(uint16_t p_106, int16_t p_107);
static int16_t func_121(uint16_t p_122, int32_t p_123);
static uint16_t func_124(struct S0 p_125, struct S0 p_126, struct S0 p_127, int32_t p_128);
static struct S0 func_129(int32_t p_130, struct S0 p_131, uint32_t p_132, int16_t p_133);
static struct S0 func_1(void)
{
    int16_t l_2[10][2] = {{4L,0x3367L},{4L,0x5ED9L},{1L,1L},{0x5ED9L,4L},{0x3367L,4L},{0x5ED9L,1L},{1L,0x5ED9L},{4L,0x3367L},{4L,0x5ED9L},{1L,1L}};
    int32_t l_34 = 0x08FBDEDBL;
    uint8_t l_2512[10] = {0x2DL,255UL,1UL,255UL,0x2DL,0x2DL,255UL,1UL,255UL,0x2DL};
    int32_t l_2548 = 0x4D1A8BEAL;
    uint16_t l_2620 = 0xFD14L;
    int32_t l_2642[4][4][3] = {{{0xCC122BAFL,0L,0L},{0L,0L,(-1L)},{7L,0xCC122BAFL,0x1B89E59DL},{0L,0L,1L}},{{0xCC122BAFL,7L,0L},{0L,0L,0L},{0L,0xCC122BAFL,0x9DD0A62BL},{0x0FA4A322L,0L,0L}},{{0x9DD0A62BL,0L,0L},{0xF320DB50L,0x0FA4A322L,1L},{0x9DD0A62BL,0x9DD0A62BL,0x1B89E59DL},{0x0FA4A322L,0xF320DB50L,(-1L)}},{{0L,0x9DD0A62BL,0L},{0L,0x0FA4A322L,0L},{0xCC122BAFL,0L,0L},{0L,0L,(-1L)}}};
    int32_t l_2715 = 0x2F2F4837L;
    struct S0 l_2815 = {0L,1L,4294967295UL,0L,0x2969L};
    int i, j, k;
    for (g_3 = 1; (g_3 >= 0); g_3 -= 1)
    {
        uint16_t l_30 = 0xF57BL;
        int32_t l_33 = 0xB5FB49A5L;
        uint32_t l_2550 = 0UL;
        int32_t l_2665 = 0L;
        int32_t l_2667[10];
        int32_t l_2710 = (-5L);
        int32_t l_2716 = 0x454A6460L;
        uint32_t l_2786[3][2][5] = {{{1UL,0UL,1UL,0UL,1UL},{4294967293UL,4294967293UL,1UL,1UL,4294967293UL}},{{0x2C014413L,0UL,0x2C014413L,0UL,0x2C014413L},{4294967293UL,1UL,1UL,4294967293UL,4294967293UL}},{{1UL,0UL,1UL,0UL,1UL},{4294967293UL,4294967293UL,1UL,1UL,4294967293UL}}};
        uint32_t l_2813[2];
        int i, j, k;
        for (i = 0; i < 10; i++)
            l_2667[i] = (-6L);
        for (i = 0; i < 2; i++)
            l_2813[i] = 0x4CE1558FL;
        for (g_4[7][0][1] = 1; (g_4[7][0][1] >= 0); g_4[7][0][1] -= 1)
        {
            int16_t l_12 = (-1L);
            uint32_t l_56[2][2][2] = {{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}},{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}}};
            int32_t l_62 = 1L;
            int32_t l_63 = 0x6F270ADFL;
            int32_t l_64 = (-1L);
            int8_t l_2549 = 0x1AL;
            struct S0 l_2556 = {0xC7L,0xCEL,0xD983B467L,-3L,0UL};
            uint16_t l_2649 = 1UL;
            struct S0 l_2750 = {4L,0x7DL,4294967294UL,0xDEDDD6A8L,3UL};
            int i, j, k;
            for (g_5[2] = 1; (g_5[2] >= 0); g_5[2] -= 1)
            {
                uint32_t l_35 = 6UL;
                int32_t l_2513 = (-1L);
                int8_t l_2552 = 4L;
                struct S0 l_2555 = {5L,-4L,4294967287UL,0xA1966BB6L,0x5237L};
                int i, j;
                l_34 = (safe_sub_func_uint8_t_u_u((l_2[(g_5[2] + 6)][g_5[2]] ^ (safe_rshift_func_int16_t_s_u((4294967286UL ^ (l_33 = (g_32 ^= ((safe_mod_func_uint8_t_u_u((l_12 > func_13(g_4[3][3][1], func_17(g_5[2], g_5[2], g_4[2][3][1], g_4[7][0][1]), l_30)), l_30)) == g_5[2])))), g_26))), 0xA2L));
                if (func_17((l_35 = l_2[(g_5[2] + 6)][g_5[2]]), func_17((safe_lshift_func_int16_t_s_s(0xCD43L, 1)), g_5[2], (g_22 &= (safe_lshift_func_int16_t_s_u((safe_rshift_func_uint8_t_u_s(l_2[9][1], 1)), 0))), (g_59[7] = (safe_rshift_func_uint16_t_u_u((l_30 > ((safe_rshift_func_int8_t_s_s(((g_58 = (g_57 = func_13((g_26 |= 5L), l_12, (safe_unary_minus_func_int16_t_s(((safe_rshift_func_int16_t_s_u(l_12, func_13((g_55[0][3] |= (safe_mul_func_uint16_t_u_u(((((safe_mul_func_uint16_t_u_u((g_32 = (safe_mod_func_int32_t_s_s((0xF0L || 0x06L), 0x8CA929EFL))), g_27)) >= l_33) > l_33) & g_3), (-4L)))), g_4[4][0][1], l_56[0][1][0]))) >= g_5[2])))))) < l_33), g_4[7][0][1])) || l_2[4][0])), 0)))), l_2[(g_5[2] + 6)][g_5[2]], g_4[7][0][1]))
                {
                    int32_t l_67 = 0L;
                    int32_t l_68 = (-10L);
                    int32_t l_94 = 0xE1143771L;
                    int8_t l_95 = 0x9AL;
                    int8_t l_2486 = 0x28L;
                    if ((safe_lshift_func_uint16_t_u_s((l_67 = (((--g_59[8]) <= g_55[0][3]) < 65535UL)), 0)))
                    {
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
l_34 = (safe_sub_func_uint8_t_u_u((l_2[(g_5[2] + 6)][g_5[2]] ^ (safe_rshift_func_int16_t_s_u((4294967286UL ^ (l_33 = (g_32 ^= ((safe_mod_func_uint8_t_u_u((l_12 > func_13(g_4[3][3][1], func_17(g_5[2], g_5[2], g_4[2][3][1], g_4[7][0][1]), l_30)), l_30)) == g_5[2])))), g_26))), 0xA2L));



                        if (l_34)
                            break;
if (l_34)
                            break;



                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }
                    else
                    {
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);
{
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
                        if (l_34)
                            break;
                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }




{
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);



                    }









l_2667[i] = (-6L);



                    }
                    for (g_465 = 0; (g_465 >= 7); ++g_465)
                    {
                        g_58 &= 0L;
                    }
                }
                else
                {
                    uint16_t l_2551 = 0x102DL;


                    return g_152[0];
                }
                g_152[0] = g_283;
{
                    int32_t l_67 = 0L;
                    int32_t l_68 = (-10L);
                    int32_t l_94 = 0xE1143771L;
                    int8_t l_95 = 0x9AL;
                    int8_t l_2486 = 0x28L;
                    if ((safe_lshift_func_uint16_t_u_s((l_67 = (((--g_59[8]) <= g_55[0][3]) < 65535UL)), 0)))
                    {
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
                        if (l_34)
                            break;
                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }
                    else
                    {
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);



                    }
                    for (g_465 = 0; (g_465 >= 7); ++g_465)
                    {
                        g_58 &= 0L;
                    }
                }





{
                uint32_t l_35 = 6UL;
                int32_t l_2513 = (-1L);
                int8_t l_2552 = 4L;
                struct S0 l_2555 = {5L,-4L,4294967287UL,0xA1966BB6L,0x5237L};
                int i, j;
                l_34 = (safe_sub_func_uint8_t_u_u((l_2[(g_5[2] + 6)][g_5[2]] ^ (safe_rshift_func_int16_t_s_u((4294967286UL ^ (l_33 = (g_32 ^= ((safe_mod_func_uint8_t_u_u((l_12 > func_13(g_4[3][3][1], func_17(g_5[2], g_5[2], g_4[2][3][1], g_4[7][0][1]), l_30)), l_30)) == g_5[2])))), g_26))), 0xA2L));
                if (func_17((l_35 = l_2[(g_5[2] + 6)][g_5[2]]), func_17((safe_lshift_func_int16_t_s_s(0xCD43L, 1)), g_5[2], (g_22 &= (safe_lshift_func_int16_t_s_u((safe_rshift_func_uint8_t_u_s(l_2[9][1], 1)), 0))), (g_59[7] = (safe_rshift_func_uint16_t_u_u((l_30 > ((safe_rshift_func_int8_t_s_s(((g_58 = (g_57 = func_13((g_26 |= 5L), l_12, (safe_unary_minus_func_int16_t_s(((safe_rshift_func_int16_t_s_u(l_12, func_13((g_55[0][3] |= (safe_mul_func_uint16_t_u_u(((((safe_mul_func_uint16_t_u_u((g_32 = (safe_mod_func_int32_t_s_s((0xF0L || 0x06L), 0x8CA929EFL))), g_27)) >= l_33) > l_33) & g_3), (-4L)))), g_4[4][0][1], l_56[0][1][0]))) >= g_5[2])))))) < l_33), g_4[7][0][1])) || l_2[4][0])), 0)))), l_2[(g_5[2] + 6)][g_5[2]], g_4[7][0][1]))
                {
                    int32_t l_67 = 0L;
                    int32_t l_68 = (-10L);
                    int32_t l_94 = 0xE1143771L;
                    int8_t l_95 = 0x9AL;
                    int8_t l_2486 = 0x28L;
                    if ((safe_lshift_func_uint16_t_u_s((l_67 = (((--g_59[8]) <= g_55[0][3]) < 65535UL)), 0)))
                    {
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
                        if (l_34)
                            break;
                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }
                    else
                    {
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);



                    }
                    for (g_465 = 0; (g_465 >= 7); ++g_465)
                    {
                        g_58 &= 0L;
                    }
                }
                else
                {
                    uint16_t l_2551 = 0x102DL;
                    if (((((safe_sub_func_uint8_t_u_u((+((safe_lshift_func_int16_t_s_u(((((safe_lshift_func_uint16_t_u_s(((g_32 | (+g_55[0][5])) || (0UL > l_2512[8])), (safe_mod_func_uint8_t_u_u(((safe_rshift_func_int8_t_s_s(0x23L, 3)) != (l_33 = (g_80 == (l_2548 = (((safe_lshift_func_uint8_t_u_u((l_30 ^ (((((l_2549 = (l_2[1][1] == (l_34 ^= (safe_mul_func_uint16_t_u_u((safe_sub_func_int8_t_s_s((l_2548 > l_2513), g_2181)), g_283.f2))))) || l_2512[8]) <= 0x821FBA5CL) == l_2550) < 0x4508L)), g_1185)) >= 0x5508F496L) <= g_203[1]))))), l_2550)))) == l_56[0][1][0]) && 0xADL) ^ l_2[(g_5[2] + 6)][g_5[2]]), 14)) | l_2551)), g_23[2])) < g_203[2]) || 0x07L) > 0xE8F1C92CL))
                    {
                        g_152[0] = func_76(l_2552, l_34, (g_1917++));
                    }
                    else
                    {
                        if (g_152[0].f0)
                            break;
                        if (l_2551)
                            break;
                        return l_2555;
                    }
                    return g_152[0];
                }
                g_152[0] = g_283;
                for (g_234 = 0; (g_234 <= 8); g_234 += 1)
                {
                    for (g_1356 = 8; (g_1356 >= 3); g_1356 -= 1)
                    {
                        g_58 ^= 5L;
                        return l_2556;
                    }
                }
            }


            }
            if ((l_33 || ((safe_mod_func_uint32_t_u_u(l_2549, g_410)) | (safe_mod_func_int8_t_s_s(((safe_rshift_func_uint8_t_u_s(0xE9L, 2)) & (0xB3L ^ l_34)), (safe_mul_func_uint16_t_u_u(((!l_2556.f1) ^ (safe_sub_func_uint32_t_u_u((safe_mul_func_int16_t_s_s(l_34, ((safe_lshift_func_int16_t_s_s(((l_33 & 255UL) <= 0x8AD0L), 10)) != l_30))), l_64))), g_214)))))))
            {
                uint8_t l_2571 = 0xA3L;
                int32_t l_2595 = (-1L);
                for (g_466 = 0; (g_466 <= 7); g_466 += 1)
                {
                    int i;
                    if ((l_2571 = g_5[g_3]))
                    {
                        int32_t l_2594 = 1L;
                        int i, j, k;
                        g_2181 = (safe_sub_func_int32_t_s_s((65530UL && l_56[g_3][g_4[7][0][1]][g_3]), l_12));

                    }
                    else
                    {




                    }
                }
            }
            else
            {
                uint16_t l_2616 = 1UL;
                int32_t l_2617 = (-1L);


            }
            if (((safe_mod_func_uint16_t_u_u((~(g_152[0].f4 >= ((5L != g_283.f1) != (l_33 = 0x57L)))), (g_1707 && g_1477))) < ((0x1A0B5C90L > l_2620) ^ l_2550)))
            {
                uint16_t l_2631 = 0xDA0EL;
                int32_t l_2635 = 0xF5206446L;
                g_152[1] = g_152[1];
                g_410 = (safe_lshift_func_int8_t_s_u(g_27, 1));

            }
            else
            {
                int16_t l_2664 = 1L;
                int32_t l_2666 = (-9L);
                int32_t l_2713 = 0x8BE2DE62L;
                int32_t l_2714[9][4][7] = {{{0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L,(-2L),0x900C9695L},{(-4L),(-4L),0L,1L,(-9L),0x74C2D1E6L,0x900C9695L},{(-9L),8L,1L,(-4L),0x900C9695L,0xFD0CBA57L,0xFD0CBA57L},{(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L),(-4L),(-9L)}},{{1L,0L,0x577BD099L,8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL},{8L,(-2L),1L,0xB4C3E57AL,0xB4C3E57AL,8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L},{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L}},{{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L},{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L}},{{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L},{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L}},{{0xBDB86FEEL,0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L},{8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL,(-4L),0xF133634EL,0xB4C3E57AL},{0x577BD099L,0x577BD099L,(-2L),8L,0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL},{1L,0xBDB86FEEL,8L,0x577BD099L,0xB4C3E57AL,0L,0L}},{{0x74C2D1E6L,(-4L),8L,(-4L),0x74C2D1E6L,0x577BD099L,1L},{1L,(-2L),8L,(-9L),(-4L),(-9L),0x38F21CE1L},{(-9L),0xF133634EL,8L,(-9L),(-9L),8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L}},{{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L},{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L}},{{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L},{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L}},{{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L},{0x900C9695L,8L,0xB4C3E57AL,0xFD0CBA57L,0x74C2D1E6L,8L,(-2L)},{(-9L),(-4L),(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L)},{8L,8L,0xF133634EL,0xBDB86FEEL,0xFD0CBA57L,0L,(-9L)}}};
                struct S0 l_2752 = {0x70L,-5L,0x75335BE2L,0xEA5BCF78L,0x0CFEL};
                int i, j, k;



l_2813[i] = 0x4CE1558FL;



                if (l_30)
                    ;

                for (g_283.f3 = 22; (g_283.f3 <= 26); g_283.f3 = safe_add_func_int16_t_s_s(g_283.f3, 7))
                {
                    uint32_t l_2717 = 4294967287UL;
                    int32_t l_2751 = 0x0816A1D2L;
                    int32_t l_2765 = 0x6072443AL;
                    uint8_t l_2785 = 255UL;


{
                uint16_t l_2631 = 0xDA0EL;
                int32_t l_2635 = 0xF5206446L;
                g_152[1] = g_152[1];
                g_410 = (safe_lshift_func_int8_t_s_u(g_27, 1));

            }


                    if ((((safe_sub_func_int8_t_s_s(((g_152[0].f0 = ((safe_unary_minus_func_uint32_t_u((((safe_mul_func_uint8_t_u_u(((((safe_unary_minus_func_uint32_t_u(0UL)) & (safe_div_func_uint16_t_u_u((safe_rshift_func_uint16_t_u_s((safe_sub_func_int32_t_s_s((l_2549 <= (safe_sub_func_uint8_t_u_u((g_2181 & 0xD8D2L), (safe_sub_func_uint8_t_u_u((safe_mul_func_int16_t_s_s((g_1185 |= 0x71F4L), (safe_div_func_uint32_t_u_u((safe_add_func_int16_t_s_s((safe_rshift_func_uint8_t_u_s((++g_55[0][3]), 6)), (l_2548 <= (safe_mod_func_int16_t_s_s(((-6L) || 0xF7L), (safe_rshift_func_uint16_t_u_u(g_283.f4, 5))))))), l_2512[8])))), 0x28L))))), g_407)), 7)), l_2556.f2))) >= l_2667[6]) && 0x5E7A6869L), 0L)) & g_5[2]) ^ g_203[0]))) & (-5L))) < l_56[1][1][0]), 0x96L)) | 253UL) >= 0x6CL))
                    {
                        uint8_t l_2766 = 0x6EL;
                        l_2750 = g_152[0];





for (i = 0; i < 10; i++)
            l_2667[i] = (-6L);



                    }
                    else
                    {
                        int32_t l_2772 = 0xBE2E81B8L;
                        if (g_3)
                            ;

{
        uint16_t l_30 = 0xF57BL;
        int32_t l_33 = 0xB5FB49A5L;
        uint32_t l_2550 = 0UL;
        int32_t l_2665 = 0L;
        int32_t l_2667[10];
        int32_t l_2710 = (-5L);
        int32_t l_2716 = 0x454A6460L;
        uint32_t l_2786[3][2][5] = {{{1UL,0UL,1UL,0UL,1UL},{4294967293UL,4294967293UL,1UL,1UL,4294967293UL}},{{0x2C014413L,0UL,0x2C014413L,0UL,0x2C014413L},{4294967293UL,1UL,1UL,4294967293UL,4294967293UL}},{{1UL,0UL,1UL,0UL,1UL},{4294967293UL,4294967293UL,1UL,1UL,4294967293UL}}};
        uint32_t l_2813[2];
        int i, j, k;
        for (i = 0; i < 10; i++)
            l_2667[i] = (-6L);
        for (i = 0; i < 2; i++)
            l_2813[i] = 0x4CE1558FL;
        for (g_4[7][0][1] = 1; (g_4[7][0][1] >= 0); g_4[7][0][1] -= 1)
        {
            int16_t l_12 = (-1L);
            uint32_t l_56[2][2][2] = {{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}},{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}}};
            int32_t l_62 = 1L;
            int32_t l_63 = 0x6F270ADFL;
            int32_t l_64 = (-1L);
            int8_t l_2549 = 0x1AL;
            struct S0 l_2556 = {0xC7L,0xCEL,0xD983B467L,-3L,0UL};
            uint16_t l_2649 = 1UL;
            struct S0 l_2750 = {4L,0x7DL,4294967294UL,0xDEDDD6A8L,3UL};
            int i, j, k;
            for (g_5[2] = 1; (g_5[2] >= 0); g_5[2] -= 1)
            {
                uint32_t l_35 = 6UL;
                int32_t l_2513 = (-1L);
                int8_t l_2552 = 4L;
                struct S0 l_2555 = {5L,-4L,4294967287UL,0xA1966BB6L,0x5237L};
                int i, j;
                l_34 = (safe_sub_func_uint8_t_u_u((l_2[(g_5[2] + 6)][g_5[2]] ^ (safe_rshift_func_int16_t_s_u((4294967286UL ^ (l_33 = (g_32 ^= ((safe_mod_func_uint8_t_u_u((l_12 > func_13(g_4[3][3][1], func_17(g_5[2], g_5[2], g_4[2][3][1], g_4[7][0][1]), l_30)), l_30)) == g_5[2])))), g_26))), 0xA2L));
                if (func_17((l_35 = l_2[(g_5[2] + 6)][g_5[2]]), func_17((safe_lshift_func_int16_t_s_s(0xCD43L, 1)), g_5[2], (g_22 &= (safe_lshift_func_int16_t_s_u((safe_rshift_func_uint8_t_u_s(l_2[9][1], 1)), 0))), (g_59[7] = (safe_rshift_func_uint16_t_u_u((l_30 > ((safe_rshift_func_int8_t_s_s(((g_58 = (g_57 = func_13((g_26 |= 5L), l_12, (safe_unary_minus_func_int16_t_s(((safe_rshift_func_int16_t_s_u(l_12, func_13((g_55[0][3] |= (safe_mul_func_uint16_t_u_u(((((safe_mul_func_uint16_t_u_u((g_32 = (safe_mod_func_int32_t_s_s((0xF0L || 0x06L), 0x8CA929EFL))), g_27)) >= l_33) > l_33) & g_3), (-4L)))), g_4[4][0][1], l_56[0][1][0]))) >= g_5[2])))))) < l_33), g_4[7][0][1])) || l_2[4][0])), 0)))), l_2[(g_5[2] + 6)][g_5[2]], g_4[7][0][1]))
                {
                    int32_t l_67 = 0L;
                    int32_t l_68 = (-10L);
                    int32_t l_94 = 0xE1143771L;
                    int8_t l_95 = 0x9AL;
                    int8_t l_2486 = 0x28L;
                    if ((safe_lshift_func_uint16_t_u_s((l_67 = (((--g_59[8]) <= g_55[0][3]) < 65535UL)), 0)))
                    {
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
                        if (l_34)
                            break;
                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }
                    else
                    {
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);



                    }
                    for (g_465 = 0; (g_465 >= 7); ++g_465)
                    {
                        g_58 &= 0L;
                    }
                }
                else
                {
                    uint16_t l_2551 = 0x102DL;
                    if (((((safe_sub_func_uint8_t_u_u((+((safe_lshift_func_int16_t_s_u(((((safe_lshift_func_uint16_t_u_s(((g_32 | (+g_55[0][5])) || (0UL > l_2512[8])), (safe_mod_func_uint8_t_u_u(((safe_rshift_func_int8_t_s_s(0x23L, 3)) != (l_33 = (g_80 == (l_2548 = (((safe_lshift_func_uint8_t_u_u((l_30 ^ (((((l_2549 = (l_2[1][1] == (l_34 ^= (safe_mul_func_uint16_t_u_u((safe_sub_func_int8_t_s_s((l_2548 > l_2513), g_2181)), g_283.f2))))) || l_2512[8]) <= 0x821FBA5CL) == l_2550) < 0x4508L)), g_1185)) >= 0x5508F496L) <= g_203[1]))))), l_2550)))) == l_56[0][1][0]) && 0xADL) ^ l_2[(g_5[2] + 6)][g_5[2]]), 14)) | l_2551)), g_23[2])) < g_203[2]) || 0x07L) > 0xE8F1C92CL))
                    {
                        g_152[0] = func_76(l_2552, l_34, (g_1917++));
                    }
                    else
                    {
                        if (g_152[0].f0)
                            break;
                        if (l_2551)
                            break;
                        return l_2555;
                    }
                    return g_152[0];
                }
                g_152[0] = g_283;
                for (g_234 = 0; (g_234 <= 8); g_234 += 1)
                {
                    for (g_1356 = 8; (g_1356 >= 3); g_1356 -= 1)
                    {
                        g_58 ^= 5L;
                        return l_2556;
                    }
                }
            }
            if ((l_33 || ((safe_mod_func_uint32_t_u_u(l_2549, g_410)) | (safe_mod_func_int8_t_s_s(((safe_rshift_func_uint8_t_u_s(0xE9L, 2)) & (0xB3L ^ l_34)), (safe_mul_func_uint16_t_u_u(((!l_2556.f1) ^ (safe_sub_func_uint32_t_u_u((safe_mul_func_int16_t_s_s(l_34, ((safe_lshift_func_int16_t_s_s(((l_33 & 255UL) <= 0x8AD0L), 10)) != l_30))), l_64))), g_214)))))))
            {
                uint8_t l_2571 = 0xA3L;
                int32_t l_2595 = (-1L);
                for (g_466 = 0; (g_466 <= 7); g_466 += 1)
                {
                    int i;
                    if ((l_2571 = g_5[g_3]))
                    {
                        int32_t l_2594 = 1L;
                        int i, j, k;
                        g_2181 = (safe_sub_func_int32_t_s_s((65530UL && l_56[g_3][g_4[7][0][1]][g_3]), l_12));

                    }
                    else
                    {
                        if (g_5[g_3])
                            break;
                        l_2595 = 1L;
                    }
                }
            }
            else
            {
                uint16_t l_2616 = 1UL;
                int32_t l_2617 = (-1L);
                l_2617 |= (((((safe_lshift_func_uint8_t_u_s(g_55[0][3], 6)) >= (((((safe_add_func_uint32_t_u_u(((safe_sub_func_uint16_t_u_u(0x3991L, 0x907DL)) > (((-3L) || ((safe_mod_func_uint8_t_u_u((safe_lshift_func_int16_t_s_u((((safe_sub_func_int32_t_s_s((g_5[2] = (l_2556.f3 = (safe_lshift_func_int16_t_s_u(((safe_mod_func_int16_t_s_s((l_2512[8] & (safe_sub_func_int8_t_s_s((-1L), (safe_rshift_func_uint16_t_u_s(l_2616, l_2616))))), 0x54C0L)) != 4294967290UL), 1)))), 0x17A9EBD9L)) < g_283.f0) <= l_2512[8]), g_152[0].f0)), 0x8FL)) == g_55[0][3])) >= g_23[2])), l_62)) >= l_33) > l_2556.f4) || g_231) && g_55[2][2])) != l_56[0][0][1]) ^ g_26) & 0xE8L);
            }
            if (((safe_mod_func_uint16_t_u_u((~(g_152[0].f4 >= ((5L != g_283.f1) != (l_33 = 0x57L)))), (g_1707 && g_1477))) < ((0x1A0B5C90L > l_2620) ^ l_2550)))
            {
                uint16_t l_2631 = 0xDA0EL;
                int32_t l_2635 = 0xF5206446L;
                g_152[1] = g_152[1];
                g_410 = (safe_lshift_func_int8_t_s_u(g_27, 1));

            }
            else
            {
                int16_t l_2664 = 1L;
                int32_t l_2666 = (-9L);
                int32_t l_2713 = 0x8BE2DE62L;
                int32_t l_2714[9][4][7] = {{{0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L,(-2L),0x900C9695L},{(-4L),(-4L),0L,1L,(-9L),0x74C2D1E6L,0x900C9695L},{(-9L),8L,1L,(-4L),0x900C9695L,0xFD0CBA57L,0xFD0CBA57L},{(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L),(-4L),(-9L)}},{{1L,0L,0x577BD099L,8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL},{8L,(-2L),1L,0xB4C3E57AL,0xB4C3E57AL,8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L},{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L}},{{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L},{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L}},{{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L},{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L}},{{0xBDB86FEEL,0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L},{8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL,(-4L),0xF133634EL,0xB4C3E57AL},{0x577BD099L,0x577BD099L,(-2L),8L,0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL},{1L,0xBDB86FEEL,8L,0x577BD099L,0xB4C3E57AL,0L,0L}},{{0x74C2D1E6L,(-4L),8L,(-4L),0x74C2D1E6L,0x577BD099L,1L},{1L,(-2L),8L,(-9L),(-4L),(-9L),0x38F21CE1L},{(-9L),0xF133634EL,8L,(-9L),(-9L),8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L}},{{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L},{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L}},{{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L},{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L}},{{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L},{0x900C9695L,8L,0xB4C3E57AL,0xFD0CBA57L,0x74C2D1E6L,8L,(-2L)},{(-9L),(-4L),(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L)},{8L,8L,0xF133634EL,0xBDB86FEEL,0xFD0CBA57L,0L,(-9L)}}};
                struct S0 l_2752 = {0x70L,-5L,0x75335BE2L,0xEA5BCF78L,0x0CFEL};
                int i, j, k;


                if (l_30)
                    continue;
                for (g_283.f3 = 22; (g_283.f3 <= 26); g_283.f3 = safe_add_func_int16_t_s_s(g_283.f3, 7))
                {
                    uint32_t l_2717 = 4294967287UL;
                    int32_t l_2751 = 0x0816A1D2L;
                    int32_t l_2765 = 0x6072443AL;
                    uint8_t l_2785 = 255UL;
                    l_2717++;
                    if ((((safe_sub_func_int8_t_s_s(((g_152[0].f0 = ((safe_unary_minus_func_uint32_t_u((((safe_mul_func_uint8_t_u_u(((((safe_unary_minus_func_uint32_t_u(0UL)) & (safe_div_func_uint16_t_u_u((safe_rshift_func_uint16_t_u_s((safe_sub_func_int32_t_s_s((l_2549 <= (safe_sub_func_uint8_t_u_u((g_2181 & 0xD8D2L), (safe_sub_func_uint8_t_u_u((safe_mul_func_int16_t_s_s((g_1185 |= 0x71F4L), (safe_div_func_uint32_t_u_u((safe_add_func_int16_t_s_s((safe_rshift_func_uint8_t_u_s((++g_55[0][3]), 6)), (l_2548 <= (safe_mod_func_int16_t_s_s(((-6L) || 0xF7L), (safe_rshift_func_uint16_t_u_u(g_283.f4, 5))))))), l_2512[8])))), 0x28L))))), g_407)), 7)), l_2556.f2))) >= l_2667[6]) && 0x5E7A6869L), 0L)) & g_5[2]) ^ g_203[0]))) & (-5L))) < l_56[1][1][0]), 0x96L)) | 253UL) >= 0x6CL))
                    {
                        uint8_t l_2766 = 0x6EL;
                        l_2750 = g_152[0];

                    }
                    else
                    {
                        int32_t l_2772 = 0xBE2E81B8L;
                        if (g_3)
                            break;
                        g_152[0].f3 = (safe_unary_minus_func_uint32_t_u(g_152[0].f2));
                        if (g_621[0][2][4])
                            break;

                    }
                    l_2765 = 0L;
                }
            }
        }
        l_2786[0][1][4]++;

        for (g_57 = 1; (g_57 >= 0); g_57 -= 1)
        {
            struct S0 l_2814 = {0x73L,8L,1UL,0x3E2EA3C6L,0xBDADL};
            int i, j;
            l_33 = l_2[(g_57 + 8)][g_3];
            g_283.f3 = l_2[(g_3 + 6)][g_57];
            return l_2814;
        }
    }





{
            int16_t l_12 = (-1L);
            uint32_t l_56[2][2][2] = {{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}},{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}}};
            int32_t l_62 = 1L;
            int32_t l_63 = 0x6F270ADFL;
            int32_t l_64 = (-1L);
            int8_t l_2549 = 0x1AL;
            struct S0 l_2556 = {0xC7L,0xCEL,0xD983B467L,-3L,0UL};
            uint16_t l_2649 = 1UL;
            struct S0 l_2750 = {4L,0x7DL,4294967294UL,0xDEDDD6A8L,3UL};
            int i, j, k;
            for (g_5[2] = 1; (g_5[2] >= 0); g_5[2] -= 1)
            {
                uint32_t l_35 = 6UL;
                int32_t l_2513 = (-1L);
                int8_t l_2552 = 4L;
                struct S0 l_2555 = {5L,-4L,4294967287UL,0xA1966BB6L,0x5237L};
                int i, j;
                l_34 = (safe_sub_func_uint8_t_u_u((l_2[(g_5[2] + 6)][g_5[2]] ^ (safe_rshift_func_int16_t_s_u((4294967286UL ^ (l_33 = (g_32 ^= ((safe_mod_func_uint8_t_u_u((l_12 > func_13(g_4[3][3][1], func_17(g_5[2], g_5[2], g_4[2][3][1], g_4[7][0][1]), l_30)), l_30)) == g_5[2])))), g_26))), 0xA2L));
                if (func_17((l_35 = l_2[(g_5[2] + 6)][g_5[2]]), func_17((safe_lshift_func_int16_t_s_s(0xCD43L, 1)), g_5[2], (g_22 &= (safe_lshift_func_int16_t_s_u((safe_rshift_func_uint8_t_u_s(l_2[9][1], 1)), 0))), (g_59[7] = (safe_rshift_func_uint16_t_u_u((l_30 > ((safe_rshift_func_int8_t_s_s(((g_58 = (g_57 = func_13((g_26 |= 5L), l_12, (safe_unary_minus_func_int16_t_s(((safe_rshift_func_int16_t_s_u(l_12, func_13((g_55[0][3] |= (safe_mul_func_uint16_t_u_u(((((safe_mul_func_uint16_t_u_u((g_32 = (safe_mod_func_int32_t_s_s((0xF0L || 0x06L), 0x8CA929EFL))), g_27)) >= l_33) > l_33) & g_3), (-4L)))), g_4[4][0][1], l_56[0][1][0]))) >= g_5[2])))))) < l_33), g_4[7][0][1])) || l_2[4][0])), 0)))), l_2[(g_5[2] + 6)][g_5[2]], g_4[7][0][1]))
                {
                    int32_t l_67 = 0L;
                    int32_t l_68 = (-10L);
                    int32_t l_94 = 0xE1143771L;
                    int8_t l_95 = 0x9AL;
                    int8_t l_2486 = 0x28L;
                    if ((safe_lshift_func_uint16_t_u_s((l_67 = (((--g_59[8]) <= g_55[0][3]) < 65535UL)), 0)))
                    {
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
                        if (l_34)
                            break;
                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }
                    else
                    {
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);



                    }
                    for (g_465 = 0; (g_465 >= 7); ++g_465)
                    {
                        g_58 &= 0L;
                    }
                }
                else
                {
                    uint16_t l_2551 = 0x102DL;
                    if (((((safe_sub_func_uint8_t_u_u((+((safe_lshift_func_int16_t_s_u(((((safe_lshift_func_uint16_t_u_s(((g_32 | (+g_55[0][5])) || (0UL > l_2512[8])), (safe_mod_func_uint8_t_u_u(((safe_rshift_func_int8_t_s_s(0x23L, 3)) != (l_33 = (g_80 == (l_2548 = (((safe_lshift_func_uint8_t_u_u((l_30 ^ (((((l_2549 = (l_2[1][1] == (l_34 ^= (safe_mul_func_uint16_t_u_u((safe_sub_func_int8_t_s_s((l_2548 > l_2513), g_2181)), g_283.f2))))) || l_2512[8]) <= 0x821FBA5CL) == l_2550) < 0x4508L)), g_1185)) >= 0x5508F496L) <= g_203[1]))))), l_2550)))) == l_56[0][1][0]) && 0xADL) ^ l_2[(g_5[2] + 6)][g_5[2]]), 14)) | l_2551)), g_23[2])) < g_203[2]) || 0x07L) > 0xE8F1C92CL))
                    {
                        g_152[0] = func_76(l_2552, l_34, (g_1917++));
                    }
                    else
                    {
                        if (g_152[0].f0)
                            break;
                        if (l_2551)
                            break;
                        return l_2555;
                    }
                    return g_152[0];
                }
                g_152[0] = g_283;
                for (g_234 = 0; (g_234 <= 8); g_234 += 1)
                {
                    for (g_1356 = 8; (g_1356 >= 3); g_1356 -= 1)
                    {
                        g_58 ^= 5L;
                        return l_2556;
                    }
                }
            }
            if ((l_33 || ((safe_mod_func_uint32_t_u_u(l_2549, g_410)) | (safe_mod_func_int8_t_s_s(((safe_rshift_func_uint8_t_u_s(0xE9L, 2)) & (0xB3L ^ l_34)), (safe_mul_func_uint16_t_u_u(((!l_2556.f1) ^ (safe_sub_func_uint32_t_u_u((safe_mul_func_int16_t_s_s(l_34, ((safe_lshift_func_int16_t_s_s(((l_33 & 255UL) <= 0x8AD0L), 10)) != l_30))), l_64))), g_214)))))))
            {
                uint8_t l_2571 = 0xA3L;
                int32_t l_2595 = (-1L);
                for (g_466 = 0; (g_466 <= 7); g_466 += 1)
                {
                    int i;
                    if ((l_2571 = g_5[g_3]))
                    {
                        int32_t l_2594 = 1L;
                        int i, j, k;
                        g_2181 = (safe_sub_func_int32_t_s_s((65530UL && l_56[g_3][g_4[7][0][1]][g_3]), l_12));

                    }
                    else
                    {
                        if (g_5[g_3])
                            break;
                        l_2595 = 1L;
                    }
                }
            }
            else
            {
                uint16_t l_2616 = 1UL;
                int32_t l_2617 = (-1L);
                l_2617 |= (((((safe_lshift_func_uint8_t_u_s(g_55[0][3], 6)) >= (((((safe_add_func_uint32_t_u_u(((safe_sub_func_uint16_t_u_u(0x3991L, 0x907DL)) > (((-3L) || ((safe_mod_func_uint8_t_u_u((safe_lshift_func_int16_t_s_u((((safe_sub_func_int32_t_s_s((g_5[2] = (l_2556.f3 = (safe_lshift_func_int16_t_s_u(((safe_mod_func_int16_t_s_s((l_2512[8] & (safe_sub_func_int8_t_s_s((-1L), (safe_rshift_func_uint16_t_u_s(l_2616, l_2616))))), 0x54C0L)) != 4294967290UL), 1)))), 0x17A9EBD9L)) < g_283.f0) <= l_2512[8]), g_152[0].f0)), 0x8FL)) == g_55[0][3])) >= g_23[2])), l_62)) >= l_33) > l_2556.f4) || g_231) && g_55[2][2])) != l_56[0][0][1]) ^ g_26) & 0xE8L);
            }
            if (((safe_mod_func_uint16_t_u_u((~(g_152[0].f4 >= ((5L != g_283.f1) != (l_33 = 0x57L)))), (g_1707 && g_1477))) < ((0x1A0B5C90L > l_2620) ^ l_2550)))
            {
                uint16_t l_2631 = 0xDA0EL;
                int32_t l_2635 = 0xF5206446L;
                g_152[1] = g_152[1];
                g_410 = (safe_lshift_func_int8_t_s_u(g_27, 1));

            }
            else
            {
                int16_t l_2664 = 1L;
                int32_t l_2666 = (-9L);
                int32_t l_2713 = 0x8BE2DE62L;
                int32_t l_2714[9][4][7] = {{{0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L,(-2L),0x900C9695L},{(-4L),(-4L),0L,1L,(-9L),0x74C2D1E6L,0x900C9695L},{(-9L),8L,1L,(-4L),0x900C9695L,0xFD0CBA57L,0xFD0CBA57L},{(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L),(-4L),(-9L)}},{{1L,0L,0x577BD099L,8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL},{8L,(-2L),1L,0xB4C3E57AL,0xB4C3E57AL,8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L},{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L}},{{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L},{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L}},{{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L},{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L}},{{0xBDB86FEEL,0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L},{8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL,(-4L),0xF133634EL,0xB4C3E57AL},{0x577BD099L,0x577BD099L,(-2L),8L,0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL},{1L,0xBDB86FEEL,8L,0x577BD099L,0xB4C3E57AL,0L,0L}},{{0x74C2D1E6L,(-4L),8L,(-4L),0x74C2D1E6L,0x577BD099L,1L},{1L,(-2L),8L,(-9L),(-4L),(-9L),0x38F21CE1L},{(-9L),0xF133634EL,8L,(-9L),(-9L),8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L}},{{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L},{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L}},{{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L},{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L}},{{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L},{0x900C9695L,8L,0xB4C3E57AL,0xFD0CBA57L,0x74C2D1E6L,8L,(-2L)},{(-9L),(-4L),(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L)},{8L,8L,0xF133634EL,0xBDB86FEEL,0xFD0CBA57L,0L,(-9L)}}};
                struct S0 l_2752 = {0x70L,-5L,0x75335BE2L,0xEA5BCF78L,0x0CFEL};
                int i, j, k;


                if (l_30)
                    continue;
                for (g_283.f3 = 22; (g_283.f3 <= 26); g_283.f3 = safe_add_func_int16_t_s_s(g_283.f3, 7))
                {
                    uint32_t l_2717 = 4294967287UL;
                    int32_t l_2751 = 0x0816A1D2L;
                    int32_t l_2765 = 0x6072443AL;
                    uint8_t l_2785 = 255UL;
                    l_2717++;
                    if ((((safe_sub_func_int8_t_s_s(((g_152[0].f0 = ((safe_unary_minus_func_uint32_t_u((((safe_mul_func_uint8_t_u_u(((((safe_unary_minus_func_uint32_t_u(0UL)) & (safe_div_func_uint16_t_u_u((safe_rshift_func_uint16_t_u_s((safe_sub_func_int32_t_s_s((l_2549 <= (safe_sub_func_uint8_t_u_u((g_2181 & 0xD8D2L), (safe_sub_func_uint8_t_u_u((safe_mul_func_int16_t_s_s((g_1185 |= 0x71F4L), (safe_div_func_uint32_t_u_u((safe_add_func_int16_t_s_s((safe_rshift_func_uint8_t_u_s((++g_55[0][3]), 6)), (l_2548 <= (safe_mod_func_int16_t_s_s(((-6L) || 0xF7L), (safe_rshift_func_uint16_t_u_u(g_283.f4, 5))))))), l_2512[8])))), 0x28L))))), g_407)), 7)), l_2556.f2))) >= l_2667[6]) && 0x5E7A6869L), 0L)) & g_5[2]) ^ g_203[0]))) & (-5L))) < l_56[1][1][0]), 0x96L)) | 253UL) >= 0x6CL))
                    {
                        uint8_t l_2766 = 0x6EL;
                        l_2750 = g_152[0];

                    }
                    else
                    {
                        int32_t l_2772 = 0xBE2E81B8L;
                        if (g_3)
                            break;
                        g_152[0].f3 = (safe_unary_minus_func_uint32_t_u(g_152[0].f2));
                        if (g_621[0][2][4])
                            break;

                    }
                    l_2765 = 0L;
                }
            }
        }




{
                    uint32_t l_2717 = 4294967287UL;
                    int32_t l_2751 = 0x0816A1D2L;
                    int32_t l_2765 = 0x6072443AL;
                    uint8_t l_2785 = 255UL;
                    l_2717++;
                    if ((((safe_sub_func_int8_t_s_s(((g_152[0].f0 = ((safe_unary_minus_func_uint32_t_u((((safe_mul_func_uint8_t_u_u(((((safe_unary_minus_func_uint32_t_u(0UL)) & (safe_div_func_uint16_t_u_u((safe_rshift_func_uint16_t_u_s((safe_sub_func_int32_t_s_s((l_2549 <= (safe_sub_func_uint8_t_u_u((g_2181 & 0xD8D2L), (safe_sub_func_uint8_t_u_u((safe_mul_func_int16_t_s_s((g_1185 |= 0x71F4L), (safe_div_func_uint32_t_u_u((safe_add_func_int16_t_s_s((safe_rshift_func_uint8_t_u_s((++g_55[0][3]), 6)), (l_2548 <= (safe_mod_func_int16_t_s_s(((-6L) || 0xF7L), (safe_rshift_func_uint16_t_u_u(g_283.f4, 5))))))), l_2512[8])))), 0x28L))))), g_407)), 7)), l_2556.f2))) >= l_2667[6]) && 0x5E7A6869L), 0L)) & g_5[2]) ^ g_203[0]))) & (-5L))) < l_56[1][1][0]), 0x96L)) | 253UL) >= 0x6CL))
                    {
                        uint8_t l_2766 = 0x6EL;
                        l_2750 = g_152[0];

                    }
                    else
                    {
                        int32_t l_2772 = 0xBE2E81B8L;
                        if (g_3)
                            break;
                        g_152[0].f3 = (safe_unary_minus_func_uint32_t_u(g_152[0].f2));
                        if (g_621[0][2][4])
                            break;

                    }
                    l_2765 = 0L;
                }




                    }


                }
{
        uint16_t l_30 = 0xF57BL;
        int32_t l_33 = 0xB5FB49A5L;
        uint32_t l_2550 = 0UL;
        int32_t l_2665 = 0L;
        int32_t l_2667[10];
        int32_t l_2710 = (-5L);
        int32_t l_2716 = 0x454A6460L;
        uint32_t l_2786[3][2][5] = {{{1UL,0UL,1UL,0UL,1UL},{4294967293UL,4294967293UL,1UL,1UL,4294967293UL}},{{0x2C014413L,0UL,0x2C014413L,0UL,0x2C014413L},{4294967293UL,1UL,1UL,4294967293UL,4294967293UL}},{{1UL,0UL,1UL,0UL,1UL},{4294967293UL,4294967293UL,1UL,1UL,4294967293UL}}};
        uint32_t l_2813[2];
        int i, j, k;
        for (i = 0; i < 10; i++)
            l_2667[i] = (-6L);
        for (i = 0; i < 2; i++)
            l_2813[i] = 0x4CE1558FL;
        for (g_4[7][0][1] = 1; (g_4[7][0][1] >= 0); g_4[7][0][1] -= 1)
        {
            int16_t l_12 = (-1L);
            uint32_t l_56[2][2][2] = {{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}},{{0xBE5697A1L,0xBE5697A1L},{0xBE5697A1L,0xBE5697A1L}}};
            int32_t l_62 = 1L;
            int32_t l_63 = 0x6F270ADFL;
            int32_t l_64 = (-1L);
            int8_t l_2549 = 0x1AL;
            struct S0 l_2556 = {0xC7L,0xCEL,0xD983B467L,-3L,0UL};
            uint16_t l_2649 = 1UL;
            struct S0 l_2750 = {4L,0x7DL,4294967294UL,0xDEDDD6A8L,3UL};
            int i, j, k;
            for (g_5[2] = 1; (g_5[2] >= 0); g_5[2] -= 1)
            {
                uint32_t l_35 = 6UL;
                int32_t l_2513 = (-1L);
                int8_t l_2552 = 4L;
                struct S0 l_2555 = {5L,-4L,4294967287UL,0xA1966BB6L,0x5237L};
                int i, j;
                l_34 = (safe_sub_func_uint8_t_u_u((l_2[(g_5[2] + 6)][g_5[2]] ^ (safe_rshift_func_int16_t_s_u((4294967286UL ^ (l_33 = (g_32 ^= ((safe_mod_func_uint8_t_u_u((l_12 > func_13(g_4[3][3][1], func_17(g_5[2], g_5[2], g_4[2][3][1], g_4[7][0][1]), l_30)), l_30)) == g_5[2])))), g_26))), 0xA2L));
                if (func_17((l_35 = l_2[(g_5[2] + 6)][g_5[2]]), func_17((safe_lshift_func_int16_t_s_s(0xCD43L, 1)), g_5[2], (g_22 &= (safe_lshift_func_int16_t_s_u((safe_rshift_func_uint8_t_u_s(l_2[9][1], 1)), 0))), (g_59[7] = (safe_rshift_func_uint16_t_u_u((l_30 > ((safe_rshift_func_int8_t_s_s(((g_58 = (g_57 = func_13((g_26 |= 5L), l_12, (safe_unary_minus_func_int16_t_s(((safe_rshift_func_int16_t_s_u(l_12, func_13((g_55[0][3] |= (safe_mul_func_uint16_t_u_u(((((safe_mul_func_uint16_t_u_u((g_32 = (safe_mod_func_int32_t_s_s((0xF0L || 0x06L), 0x8CA929EFL))), g_27)) >= l_33) > l_33) & g_3), (-4L)))), g_4[4][0][1], l_56[0][1][0]))) >= g_5[2])))))) < l_33), g_4[7][0][1])) || l_2[4][0])), 0)))), l_2[(g_5[2] + 6)][g_5[2]], g_4[7][0][1]))
                {
                    int32_t l_67 = 0L;
                    int32_t l_68 = (-10L);
                    int32_t l_94 = 0xE1143771L;
                    int8_t l_95 = 0x9AL;
                    int8_t l_2486 = 0x28L;
                    if ((safe_lshift_func_uint16_t_u_s((l_67 = (((--g_59[8]) <= g_55[0][3]) < 65535UL)), 0)))
                    {
                        int i, j;
                        if (l_2[3][1])
                            break;
                        ++g_69;
                        if (l_34)
                            break;
                        l_34 = (func_72(func_76(l_2[(g_5[2] + 6)][g_5[2]], (g_81[2] |= (g_80 ^= g_32)), ((safe_sub_func_uint32_t_u_u((safe_add_func_int8_t_s_s((safe_rshift_func_int8_t_s_u(g_59[7], 5)), (safe_sub_func_int8_t_s_s(l_2[(g_5[2] + 6)][g_5[2]], (safe_mul_func_uint16_t_u_u(((safe_mod_func_int8_t_s_s(func_17(g_3, g_26, g_22, (!((func_13((l_33 = l_68), (l_94 = (g_23[2] | l_63)), g_58) < l_67) && l_2[3][0]))), 0xFFL)) == g_5[2]), l_95)))))), g_3)) & l_2[(g_5[2] + 1)][g_4[7][0][1]])), g_55[0][3], g_4[7][0][1]) <= 0xB7L);
                    }
                    else
                    {
                        int8_t l_2469 = (-1L);
                        int32_t l_2487 = (-9L);
                        l_33 = (l_2469 <= 0xA6511E7AL);



                    }
                    for (g_465 = 0; (g_465 >= 7); ++g_465)
                    {
                        g_58 &= 0L;
                    }
                }
                else
                {
                    uint16_t l_2551 = 0x102DL;
                    if (((((safe_sub_func_uint8_t_u_u((+((safe_lshift_func_int16_t_s_u(((((safe_lshift_func_uint16_t_u_s(((g_32 | (+g_55[0][5])) || (0UL > l_2512[8])), (safe_mod_func_uint8_t_u_u(((safe_rshift_func_int8_t_s_s(0x23L, 3)) != (l_33 = (g_80 == (l_2548 = (((safe_lshift_func_uint8_t_u_u((l_30 ^ (((((l_2549 = (l_2[1][1] == (l_34 ^= (safe_mul_func_uint16_t_u_u((safe_sub_func_int8_t_s_s((l_2548 > l_2513), g_2181)), g_283.f2))))) || l_2512[8]) <= 0x821FBA5CL) == l_2550) < 0x4508L)), g_1185)) >= 0x5508F496L) <= g_203[1]))))), l_2550)))) == l_56[0][1][0]) && 0xADL) ^ l_2[(g_5[2] + 6)][g_5[2]]), 14)) | l_2551)), g_23[2])) < g_203[2]) || 0x07L) > 0xE8F1C92CL))
                    {
                        g_152[0] = func_76(l_2552, l_34, (g_1917++));
                    }
                    else
                    {
                        if (g_152[0].f0)
                            break;
                        if (l_2551)
                            break;
                        return l_2555;
                    }
                    return g_152[0];
                }
                g_152[0] = g_283;
                for (g_234 = 0; (g_234 <= 8); g_234 += 1)
                {
                    for (g_1356 = 8; (g_1356 >= 3); g_1356 -= 1)
                    {
                        g_58 ^= 5L;
                        return l_2556;
                    }
                }
            }
            if ((l_33 || ((safe_mod_func_uint32_t_u_u(l_2549, g_410)) | (safe_mod_func_int8_t_s_s(((safe_rshift_func_uint8_t_u_s(0xE9L, 2)) & (0xB3L ^ l_34)), (safe_mul_func_uint16_t_u_u(((!l_2556.f1) ^ (safe_sub_func_uint32_t_u_u((safe_mul_func_int16_t_s_s(l_34, ((safe_lshift_func_int16_t_s_s(((l_33 & 255UL) <= 0x8AD0L), 10)) != l_30))), l_64))), g_214)))))))
            {
                uint8_t l_2571 = 0xA3L;
                int32_t l_2595 = (-1L);
                for (g_466 = 0; (g_466 <= 7); g_466 += 1)
                {
                    int i;
                    if ((l_2571 = g_5[g_3]))
                    {
                        int32_t l_2594 = 1L;
                        int i, j, k;
                        g_2181 = (safe_sub_func_int32_t_s_s((65530UL && l_56[g_3][g_4[7][0][1]][g_3]), l_12));

                    }
                    else
                    {
                        if (g_5[g_3])
                            break;
                        l_2595 = 1L;
                    }
                }
            }
            else
            {
                uint16_t l_2616 = 1UL;
                int32_t l_2617 = (-1L);
                l_2617 |= (((((safe_lshift_func_uint8_t_u_s(g_55[0][3], 6)) >= (((((safe_add_func_uint32_t_u_u(((safe_sub_func_uint16_t_u_u(0x3991L, 0x907DL)) > (((-3L) || ((safe_mod_func_uint8_t_u_u((safe_lshift_func_int16_t_s_u((((safe_sub_func_int32_t_s_s((g_5[2] = (l_2556.f3 = (safe_lshift_func_int16_t_s_u(((safe_mod_func_int16_t_s_s((l_2512[8] & (safe_sub_func_int8_t_s_s((-1L), (safe_rshift_func_uint16_t_u_s(l_2616, l_2616))))), 0x54C0L)) != 4294967290UL), 1)))), 0x17A9EBD9L)) < g_283.f0) <= l_2512[8]), g_152[0].f0)), 0x8FL)) == g_55[0][3])) >= g_23[2])), l_62)) >= l_33) > l_2556.f4) || g_231) && g_55[2][2])) != l_56[0][0][1]) ^ g_26) & 0xE8L);
            }
            if (((safe_mod_func_uint16_t_u_u((~(g_152[0].f4 >= ((5L != g_283.f1) != (l_33 = 0x57L)))), (g_1707 && g_1477))) < ((0x1A0B5C90L > l_2620) ^ l_2550)))
            {
                uint16_t l_2631 = 0xDA0EL;
                int32_t l_2635 = 0xF5206446L;
                g_152[1] = g_152[1];
                g_410 = (safe_lshift_func_int8_t_s_u(g_27, 1));

            }
            else
            {
                int16_t l_2664 = 1L;
                int32_t l_2666 = (-9L);
                int32_t l_2713 = 0x8BE2DE62L;
                int32_t l_2714[9][4][7] = {{{0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L,(-2L),0x900C9695L},{(-4L),(-4L),0L,1L,(-9L),0x74C2D1E6L,0x900C9695L},{(-9L),8L,1L,(-4L),0x900C9695L,0xFD0CBA57L,0xFD0CBA57L},{(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L),(-4L),(-9L)}},{{1L,0L,0x577BD099L,8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL},{8L,(-2L),1L,0xB4C3E57AL,0xB4C3E57AL,8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L},{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L}},{{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L},{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L}},{{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L},{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L}},{{0xBDB86FEEL,0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L},{8L,0x38F21CE1L,0xB4C3E57AL,0xF133634EL,(-4L),0xF133634EL,0xB4C3E57AL},{0x577BD099L,0x577BD099L,(-2L),8L,0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL},{1L,0xBDB86FEEL,8L,0x577BD099L,0xB4C3E57AL,0L,0L}},{{0x74C2D1E6L,(-4L),8L,(-4L),0x74C2D1E6L,0x577BD099L,1L},{1L,(-2L),8L,(-9L),(-4L),(-9L),0x38F21CE1L},{(-9L),0xF133634EL,8L,(-9L),(-9L),8L,0xF133634EL},{1L,(-9L),(-2L),1L,0xBDB86FEEL,8L,0x577BD099L}},{{0x74C2D1E6L,0xFD0CBA57L,0xB4C3E57AL,8L,0x900C9695L,(-9L),0x900C9695L},{1L,0x900C9695L,0x900C9695L,1L,0L,0x577BD099L,8L},{0x577BD099L,0x900C9695L,0x74C2D1E6L,(-9L),1L,0L,(-4L)},{8L,0xFD0CBA57L,0x577BD099L,(-9L),0x577BD099L,0xFD0CBA57L,8L}},{{0xBDB86FEEL,(-9L),0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L},{0x38F21CE1L,0xF133634EL,(-9L),0x577BD099L,1L,1L,0x577BD099L},{0xFD0CBA57L,(-2L),0xFD0CBA57L,8L,0L,0x38F21CE1L,0xF133634EL},{0xFD0CBA57L,(-4L),0x577BD099L,0xF133634EL,0x900C9695L,(-2L),0x38F21CE1L}},{{0x38F21CE1L,0xBDB86FEEL,0x74C2D1E6L,0x74C2D1E6L,0xBDB86FEEL,0x38F21CE1L,1L},{0x900C9695L,8L,0xB4C3E57AL,0xFD0CBA57L,0x74C2D1E6L,8L,(-2L)},{(-9L),(-4L),(-9L),0x38F21CE1L,0x577BD099L,0x38F21CE1L,(-9L)},{8L,8L,0xF133634EL,0xBDB86FEEL,0xFD0CBA57L,0L,(-9L)}}};
                struct S0 l_2752 = {0x70L,-5L,0x75335BE2L,0xEA5BCF78L,0x0CFEL};
                int i, j, k;


                if (l_30)
                    continue;
                for (g_283.f3 = 22; (g_283.f3 <= 26); g_283.f3 = safe_add_func_int16_t_s_s(g_283.f3, 7))
                {
                    uint32_t l_2717 = 4294967287UL;
                    int32_t l_2751 = 0x0816A1D2L;
                    int32_t l_2765 = 0x6072443AL;
                    uint8_t l_2785 = 255UL;
                    l_2717++;
                    if ((((safe_sub_func_int8_t_s_s(((g_152[0].f0 = ((safe_unary_minus_func_uint32_t_u((((safe_mul_func_uint8_t_u_u(((((safe_unary_minus_func_uint32_t_u(0UL)) & (safe_div_func_uint16_t_u_u((safe_rshift_func_uint16_t_u_s((safe_sub_func_int32_t_s_s((l_2549 <= (safe_sub_func_uint8_t_u_u((g_2181 & 0xD8D2L), (safe_sub_func_uint8_t_u_u((safe_mul_func_int16_t_s_s((g_1185 |= 0x71F4L), (safe_div_func_uint32_t_u_u((safe_add_func_int16_t_s_s((safe_rshift_func_uint8_t_u_s((++g_55[0][3]), 6)), (l_2548 <= (safe_mod_func_int16_t_s_s(((-6L) || 0xF7L), (safe_rshift_func_uint16_t_u_u(g_283.f4, 5))))))), l_2512[8])))), 0x28L))))), g_407)), 7)), l_2556.f2))) >= l_2667[6]) && 0x5E7A6869L), 0L)) & g_5[2]) ^ g_203[0]))) & (-5L))) < l_56[1][1][0]), 0x96L)) | 253UL) >= 0x6CL))
                    {
                        uint8_t l_2766 = 0x6EL;
                        l_2750 = g_152[0];

                    }
                    else
                    {
                        int32_t l_2772 = 0xBE2E81B8L;
                        if (g_3)
                            break;
                        g_152[0].f3 = (safe_unary_minus_func_uint32_t_u(g_152[0].f2));
                        if (g_621[0][2][4])
                            break;

                    }
                    l_2765 = 0L;
                }
            }
        }
        l_2786[0][1][4]++;

        for (g_57 = 1; (g_57 >= 0); g_57 -= 1)
        {
            struct S0 l_2814 = {0x73L,8L,1UL,0x3E2EA3C6L,0xBDADL};
            int i, j;
            l_33 = l_2[(g_57 + 8)][g_3];
            g_283.f3 = l_2[(g_3 + 6)][g_57];
            return l_2814;
        }
    }



            }
        }
        l_2786[0][1][4]++;

        for (g_57 = 1; (g_57 >= 0); g_57 -= 1)
        {
            struct S0 l_2814 = {0x73L,8L,1UL,0x3E2EA3C6L,0xBDADL};
            int i, j;
            l_33 = l_2[(g_57 + 8)][g_3];
            g_283.f3 = l_2[(g_3 + 6)][g_57];
            return l_2814;
        }
    }
    return l_2815;
}







static uint16_t func_13(int8_t p_14, int32_t p_15, uint32_t p_16)
{
    int8_t l_31 = 1L;
    return l_31;
}







static int32_t func_17(int32_t p_18, uint16_t p_19, uint8_t p_20, uint32_t p_21)
{
    uint16_t l_24 = 0x9F3BL;
    int32_t l_25 = 8L;
    g_22 |= p_20;
    l_24 ^= (g_23[2] = p_20);
    g_27++;
    l_25 |= l_24;
    return g_3;
}







static uint8_t func_72(struct S0 p_73, uint32_t p_74, int32_t p_75)
{
    uint32_t l_2457 = 1UL;


    for (p_73.f0 = 0; (p_73.f0 >= (-8)); --p_73.f0)
    {


    }






    return p_74;
}







static struct S0 func_76(uint32_t p_77, int16_t p_78, uint8_t p_79)
{
    int32_t l_98 = (-10L);
    struct S0 l_2436 = {6L,-2L,1UL,0x18035F9BL,65528UL};


{
    int32_t l_98 = (-10L);
    struct S0 l_2436 = {6L,-2L,1UL,0x18035F9BL,65528UL};
    g_152[0].f3 = (l_98 = (safe_sub_func_uint32_t_u_u((func_17(l_98, g_55[3][5], func_99((p_78 >= (safe_rshift_func_uint8_t_u_s(((safe_mod_func_int16_t_s_s(func_17(p_79, p_78, (func_17(g_27, ((func_13(g_23[2], l_98, l_98) >= 4L) >= p_79), g_5[0], g_23[2]) ^ l_98), p_78), l_98)) < p_78), 1)))), p_77) >= 1L), g_621[0][6][4])));
    return l_2436;
}


    return l_2436;
}







static uint8_t func_99(uint32_t p_100)
{
    uint8_t l_110[7][7] = {{0xFFL,0x31L,0xFFL,0x31L,0xFFL,0x31L,0xFFL},{0x78L,0x78L,0x27L,0x27L,0x78L,0x78L,0x27L},{255UL,0x31L,255UL,0x31L,255UL,0x31L,255UL},{0x78L,0x27L,0x27L,0x78L,0x78L,0x27L,0x27L},{0xFFL,0x31L,0xFFL,0x31L,0xFFL,0x31L,0xFFL},{0x78L,0x78L,0x27L,0x27L,0x78L,0x78L,0x27L},{255UL,0x31L,255UL,0x31L,255UL,0x31L,255UL}};
    int32_t l_142 = (-1L);
    int32_t l_143 = 0xEB29FA79L;
    int32_t l_144[2][9] = {{(-2L),(-2L),(-2L),(-2L),(-2L),(-2L),(-2L),(-2L),(-2L)},{0L,0L,0L,0L,0L,0L,0L,0L,0L}};
    int32_t l_145[6];
    int32_t l_146 = 0x586F400AL;
    struct S0 l_147 = {-5L,0L,0xB65799C7L,0x5F5692BDL,65528UL};
    uint32_t l_148 = 4294967295UL;
    int16_t l_2229 = 0x8A5EL;
    uint32_t l_2338 = 0xA78D6BD7L;
    int32_t l_2344 = 0x936F19A1L;
    uint16_t l_2346 = 0x1E6CL;
    int8_t l_2355 = 0x8EL;
    uint16_t l_2396 = 0x406AL;
    int32_t l_2404 = 0x8BD9194AL;
    uint8_t l_2423 = 0xFEL;
    int8_t l_2435 = (-2L);
    int i, j;


for (i = 0; i < 6; i++)
        l_145[i] = 0xE41B645FL;


    if (((~func_105((safe_rshift_func_uint8_t_u_s(l_110[5][6], (4294967295UL & (safe_rshift_func_uint16_t_u_s((safe_mod_func_uint32_t_u_u(1UL, (p_100 ^ l_110[6][2]))), 0))))), (((safe_div_func_uint32_t_u_u(((((safe_lshift_func_uint8_t_u_s(l_110[5][6], 2)) | p_100) < (safe_lshift_func_int16_t_s_s((l_144[0][0] = func_121((g_203[2] = func_124(func_129(((safe_rshift_func_int16_t_s_s((safe_lshift_func_uint8_t_u_s((((l_146 = (l_145[2] = (l_144[0][0] = (0x2B768FFDL <= (safe_lshift_func_int8_t_s_u((safe_add_func_int8_t_s_s((((l_143 = (((l_142 = p_100) && g_80) || 0xFE75L)) < p_100) == g_80), 0xA4L)), 7)))))) == g_81[2]) & 0x7E50L), p_100)), p_100)) && p_100), l_147, l_148, l_110[0][0]), g_283, l_147, p_100)), l_148)), l_110[5][6]))) != l_147.f4), g_3)) | g_55[1][5]) | g_4[7][0][1]))) == p_100))
    {
        int16_t l_2176 = (-10L);
        int32_t l_2192 = 1L;
        int32_t l_2199 = 0L;
        int32_t l_2201 = 0x582BCF30L;
        uint8_t l_2283[8] = {0xE1L,0xE1L,0x7DL,0xE1L,0xE1L,0x7DL,0xE1L,0xE1L};
        int32_t l_2307[5];
        struct S0 l_2341 = {1L,1L,4294967295UL,-1L,4UL};
        int32_t l_2343 = 3L;
        int32_t l_2345[6];
        int i;
        for (i = 0; i < 5; i++)
            {
l_2307[i] = 0xA8D90AD4L;
for (i = 0; i < 5; i++)
            l_2307[i] = 0xA8D90AD4L;



for (i = 0; i < 6; i++)
        l_145[i] = 0xE41B645FL;

}




lbl_2342:

        l_2346++;
l_2346++;



    }
    else
    {
        uint16_t l_2361 = 0xF1BCL;
        int32_t l_2392 = 0x3B3C7727L;
        int32_t l_2393 = (-1L);
        uint32_t l_2399 = 4294967292UL;
        int32_t l_2402 = 1L;
        int32_t l_2403 = 0xA722E9CDL;
        int32_t l_2405 = 0x1F0D8D51L;
        uint16_t l_2406 = 6UL;




--l_2399;




for (l_147.f1 = 8; (l_147.f1 >= (-3)); l_147.f1 = safe_sub_func_uint16_t_u_u(l_147.f1, 3))
        {
            int32_t l_2358 = 0x9556BEA6L;
            int32_t l_2394 = 2L;
            int32_t l_2395[3][7][5] = {{{1L,(-8L),1L,6L,1L},{0L,0L,4L,0xFA295410L,1L},{1L,0x1337ECABL,1L,1L,0x1337ECABL},{0x3D0099F7L,(-5L),4L,1L,0xD9C63115L},{(-8L),(-6L),1L,0xB774A815L,(-1L)},{0xAEE37CD5L,0x3D0099F7L,0x3D0099F7L,0xAEE37CD5L,0x7F888DD7L},{(-8L),1L,0xB5E344B0L,3L,0xB774A815L}},{{0x3D0099F7L,0x9725E237L,0L,4L,0L},{1L,1L,0xB774A815L,3L,0xB5E344B0L},{0L,0xFA295410L,0x7F888DD7L,0xAEE37CD5L,0x3D0099F7L},{1L,0xB774A815L,(-1L),0xB774A815L,1L},{0xE77D5347L,0xFA295410L,0xD9C63115L,1L,4L},{3L,1L,0x1337ECABL,1L,1L},{1L,0x9725E237L,1L,0xFA295410L,4L}},{{(-8L),1L,1L,6L,1L},{4L,0x3D0099F7L,0x3D0099F7L,0x3D0099F7L,0xAEE37CD5L},{8L,0xB5E344B0L,0xB774A815L,1L,(-1L)},{0xE77D5347L,0xD9C63115L,0L,0x9725E237L,0L},{1L,8L,8L,1L,(-8L)},{0xE77D5347L,0x3D0099F7L,0L,0xFA295410L,0x9725E237L},{8L,3L,(-8L),0xB774A815L,(-8L)}}};
            int i, j, k;


            l_2396++;
            return g_465;
        }


    }
for (i = 0; i < 6; i++)
        l_145[i] = 0xE41B645FL;








    g_2432--;
for (i = 0; i < 6; i++)
        l_145[i] = 0xE41B645FL;



    g_283.f3 ^= (g_58 & l_2435);
{
        uint16_t l_2361 = 0xF1BCL;
        int32_t l_2392 = 0x3B3C7727L;
        int32_t l_2393 = (-1L);
        uint32_t l_2399 = 4294967292UL;
        int32_t l_2402 = 1L;
        int32_t l_2403 = 0xA722E9CDL;
        int32_t l_2405 = 0x1F0D8D51L;
        uint16_t l_2406 = 6UL;
        for (l_147.f1 = 8; (l_147.f1 >= (-3)); l_147.f1 = safe_sub_func_uint16_t_u_u(l_147.f1, 3))
        {
            int32_t l_2358 = 0x9556BEA6L;
            int32_t l_2394 = 2L;
            int32_t l_2395[3][7][5] = {{{1L,(-8L),1L,6L,1L},{0L,0L,4L,0xFA295410L,1L},{1L,0x1337ECABL,1L,1L,0x1337ECABL},{0x3D0099F7L,(-5L),4L,1L,0xD9C63115L},{(-8L),(-6L),1L,0xB774A815L,(-1L)},{0xAEE37CD5L,0x3D0099F7L,0x3D0099F7L,0xAEE37CD5L,0x7F888DD7L},{(-8L),1L,0xB5E344B0L,3L,0xB774A815L}},{{0x3D0099F7L,0x9725E237L,0L,4L,0L},{1L,1L,0xB774A815L,3L,0xB5E344B0L},{0L,0xFA295410L,0x7F888DD7L,0xAEE37CD5L,0x3D0099F7L},{1L,0xB774A815L,(-1L),0xB774A815L,1L},{0xE77D5347L,0xFA295410L,0xD9C63115L,1L,4L},{3L,1L,0x1337ECABL,1L,1L},{1L,0x9725E237L,1L,0xFA295410L,4L}},{{(-8L),1L,1L,6L,1L},{4L,0x3D0099F7L,0x3D0099F7L,0x3D0099F7L,0xAEE37CD5L},{8L,0xB5E344B0L,0xB774A815L,1L,(-1L)},{0xE77D5347L,0xD9C63115L,0L,0x9725E237L,0L},{1L,8L,8L,1L,(-8L)},{0xE77D5347L,0x3D0099F7L,0L,0xFA295410L,0x9725E237L},{8L,3L,(-8L),0xB774A815L,(-8L)}}};
            int i, j, k;


            l_2396++;
            return g_465;
        }
        --l_2399;
        l_2406--;
    }



    return p_100;
}







static uint32_t func_105(uint16_t p_106, int16_t p_107)
{
    uint16_t l_1887 = 0x1DFFL;
    uint8_t l_1915 = 0x32L;
    int32_t l_1930 = 8L;
    int32_t l_1931[4][5];
    uint32_t l_1938 = 4UL;
    int32_t l_2133 = 0L;
    struct S0 l_2172 = {0x61L,-1L,4294967286UL,0x13E044E4L,65530UL};
    int i, j;


for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 5; j++)
            l_1931[i][j] = 2L;
    }


lbl_2101:
    g_152[0].f3 = 0L;


for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 5; j++)
            l_1931[i][j] = 2L;
    }




for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 5; j++)
            l_1931[i][j] = 2L;
    }




    return g_23[2];
}







static int16_t func_121(uint16_t p_122, int32_t p_123)
{
    int32_t l_292 = (-7L);
    int8_t l_304[9] = {1L,(-10L),(-10L),1L,(-10L),(-10L),1L,(-10L),(-10L)};
    int32_t l_345 = 0x7D3ECDBFL;
    int32_t l_347[8] = {0x4EB9A496L,0L,0L,0x4EB9A496L,0L,0L,0x4EB9A496L,0L};
    int32_t l_369 = 0xA03A67FCL;
    uint16_t l_437 = 65535UL;
    uint16_t l_516 = 0UL;
    uint16_t l_624[7] = {0xED81L,0xED81L,65535UL,0xED81L,0xED81L,65535UL,0xED81L};
    int8_t l_719 = 0xB7L;
    uint32_t l_845 = 0UL;
    uint32_t l_866[2][8] = {{4294967287UL,4294967287UL,1UL,4294967293UL,1UL,4294967287UL,4294967287UL,1UL},{4294967295UL,1UL,1UL,4294967295UL,0x49E6E4D0L,4294967295UL,1UL,1UL}};
    struct S0 l_867 = {0x9CL,0x48L,0xD831EC18L,-6L,0x7EAAL};
    uint32_t l_956 = 3UL;
    uint8_t l_971 = 0x64L;
    int32_t l_1012 = 0xF2E34BE1L;
    int32_t l_1172 = 0L;
    uint16_t l_1359 = 65526UL;
    uint32_t l_1385 = 0xAC7D7E04L;
    int16_t l_1502 = (-1L);
    int16_t l_1606 = 0x16D7L;
    uint8_t l_1704 = 0x4FL;
    int8_t l_1801 = (-1L);
    int32_t l_1855 = 0x6FD1A748L;
    uint32_t l_1860 = 0xF717CB91L;
    uint8_t l_1871 = 1UL;
    uint32_t l_1872[1][4] = {{0x2CAFB76BL,0x2CAFB76BL,0x2CAFB76BL,0x2CAFB76BL}};
    int i, j;
lbl_1305:
    if ((safe_unary_minus_func_uint32_t_u(g_57)))
    {
        struct S0 l_285 = {0x62L,0x63L,0x80A18275L,0x3D69D35CL,1UL};
        int32_t l_303 = (-2L);
        int32_t l_519 = 0xCF0C64A2L;
        int32_t l_594 = 1L;
        int32_t l_622 = 0x0C42AC63L;
        int8_t l_720 = 4L;
        int16_t l_740 = 0L;
        uint32_t l_834 = 4294967287UL;
        int32_t l_846 = 0x25424842L;
        for (g_231 = 0; (g_231 <= 8); g_231 += 1)
        {
            uint16_t l_307 = 65533UL;
            int32_t l_365 = 3L;
            int32_t l_507[1];
            uint8_t l_528 = 0x94L;
            uint32_t l_590[7];
            uint32_t l_603 = 0x9AED675AL;
            int32_t l_612 = 0L;
            int32_t l_659 = 0L;
            uint16_t l_739 = 0UL;
            uint16_t l_758[9][1][9] = {{{65535UL,0UL,1UL,0UL,1UL,4UL,1UL,0UL,1UL}},{{0x9B2EL,0x9B2EL,1UL,0UL,1UL,1UL,0x3497L,0xFE5AL,0xC69EL}},{{0UL,0xBF4CL,0xFE5AL,0xC4F1L,0x36C1L,0x1146L,65535UL,1UL,1UL}},{{0xC69EL,0x21C9L,1UL,0x36C1L,1UL,0x21C9L,0xC69EL,0x12FCL,0x8601L}},{{0xC69EL,65535UL,1UL,0x21C9L,0UL,0UL,0x1146L,4UL,0UL}},{{0UL,1UL,0UL,65535UL,0x12FCL,0UL,0UL,0x12FCL,65535UL}},{{0x9B2EL,0UL,0x9B2EL,0x8601L,0xBF4CL,0UL,0x36C1L,1UL,1UL}},{{65535UL,65535UL,0xBF4CL,1UL,4UL,0UL,0UL,0xFE5AL,0x1146L}},{{0UL,0xC4F1L,0x21C9L,0x8601L,0x8601L,0x21C9L,0xC4F1L,0UL,0x9B2EL}}};
            int32_t l_778 = (-6L);
            struct S0 l_847 = {-2L,0xFEL,0xB66DDDD8L,0xD80953FEL,1UL};
            int i, j, k;
            for (i = 0; i < 1; i++)
                l_507[i] = (-1L);
            for (i = 0; i < 7; i++)
                l_590[i] = 4294967289UL;
            l_285 = l_285;
            if (((((g_59[g_231] != (l_303 = (safe_div_func_int8_t_s_s((safe_sub_func_int32_t_s_s(g_59[g_231], (safe_mod_func_uint32_t_u_u(l_292, (safe_rshift_func_int16_t_s_u(((safe_mod_func_uint32_t_u_u((l_285.f3 = (((((0L < (safe_sub_func_uint8_t_u_u(0xD9L, (safe_lshift_func_int8_t_s_s((safe_div_func_uint16_t_u_u(g_152[0].f4, p_122)), p_123))))) != g_4[6][1][1]) | g_234) <= g_59[g_231]) != g_231)), 0x393EE34DL)) < 0x1DCF8AABL), g_4[6][3][0])))))), g_3)))) != l_292) | p_122) != l_304[8]))
            {
                uint32_t l_368 = 0xF8D497B3L;
                int8_t l_385 = 0xBFL;
                int32_t l_404 = 0x22424442L;
                int32_t l_515 = 0xA3940CC9L;
                for (l_285.f2 = 0; (l_285.f2 <= 3); l_285.f2 += 1)
                {
                    int i;
                    return g_81[l_285.f2];
                }
                for (p_123 = (-30); (p_123 >= (-11)); ++p_123)
                {
                    uint32_t l_310[5] = {0x7972E57FL,0x7972E57FL,0x7972E57FL,0x7972E57FL,0x7972E57FL};
                    int32_t l_346[10] = {3L,0xFD91DCD4L,3L,3L,0xFD91DCD4L,3L,3L,0xFD91DCD4L,3L,3L};
                    int32_t l_348 = 0xC0335DBAL;
                    int i;
                    if (l_307)
                        break;

                    return l_285.f2;
                }


            }
            else
            {
                uint32_t l_606 = 1UL;
                int32_t l_607 = 0L;
                int32_t l_609 = 0x9EC9A96BL;
                int32_t l_611 = 0xD4F35AACL;
                int32_t l_613 = 1L;
                int32_t l_614 = 0x60EB540DL;
                int32_t l_618 = 1L;
                int32_t l_620 = 6L;
                int32_t l_623 = 0xA5C257B2L;
                struct S0 l_682 = {0xB5L,0xE5L,0x71A8812CL,-1L,65535UL};
                uint8_t l_751 = 1UL;

                g_80 = (((safe_lshift_func_uint8_t_u_s(l_307, (safe_mul_func_uint8_t_u_u(l_292, 0xB2L)))) && (((g_32 = g_59[7]) | (safe_lshift_func_uint8_t_u_u((safe_lshift_func_uint8_t_u_u((((safe_mod_func_uint32_t_u_u(((p_123 < (l_347[1] ^= 0x64D6BBBBL)) && (safe_add_func_int16_t_s_s(((g_59[1] < (l_618 = (safe_lshift_func_int8_t_s_s((~((l_739 = (safe_mod_func_uint8_t_u_u(((g_234 >= ((safe_mod_func_int32_t_s_s(0L, g_203[2])) && 0x7ABEDC6EL)) || l_345), 0xDDL))) != 0x45DAL)), l_740)))) & 6UL), 1L))), 0x96CDF6C1L)) >= g_27) <= 0x4933L), p_123)), g_621[1][3][0]))) == 0L)) & g_81[1]);

            }
            if (((p_122 < 0x614BL) && ((g_59[g_231] >= (((((p_122 ^= (safe_mul_func_uint16_t_u_u(((((safe_sub_func_uint32_t_u_u((g_407 ^= l_739), (safe_mod_func_int16_t_s_s(((safe_mod_func_int8_t_s_s(((safe_rshift_func_uint8_t_u_s((safe_mul_func_uint16_t_u_u(((safe_add_func_int32_t_s_s((l_365 |= ((l_347[4] = l_758[2][0][3]) > (safe_unary_minus_func_int32_t_s((((g_32 = ((!(0xCCL || l_292)) | l_519)) == l_603) && 0x01D9L))))), 0xCB5C66CBL)) & l_624[3]), l_847.f4)), 4)) & (-8L)), 3L)) >= l_303), 65535UL)))) & l_594) | l_866[1][4]) | 0xF760L), l_847.f0))) == g_152[0].f3) | l_847.f0) > 0L) | g_551)) > 0xBDB0L)))
            {
                l_867 = (l_285 = g_283);
                for (g_214 = (-14); (g_214 == 26); g_214++)
                {
                    for (l_720 = 0; (l_720 <= 2); l_720 += 1)
                    {
                        int i;
                        g_616[l_720] = g_616[(l_720 + 2)];
                    }
                }
                l_847 = l_867;
            }
            else
            {
                struct S0 l_870 = {-6L,-1L,4294967290UL,0xE1087EE6L,4UL};
                int16_t l_906 = (-5L);
                for (l_847.f1 = 0; (l_847.f1 <= 0); l_847.f1 += 1)
                {
                    int32_t l_875[4];
                    int i;
                    for (i = 0; i < 4; i++)
                        l_875[i] = 8L;
                    g_283 = l_870;
                    for (l_845 = 0; (l_845 <= 1); l_845 += 1)
                    {
                        int32_t l_871 = 0x8B850916L;
                        int32_t l_872 = 1L;
                        int32_t l_873 = (-10L);
                        int32_t l_874[6][6][4] = {{{0xE2C58FA0L,3L,1L,0xE2C58FA0L},{0x345A5EF8L,3L,1L,3L},{3L,0xB75A3807L,0xFB524446L,(-3L)},{0xE187876CL,0x345A5EF8L,1L,0xFB524446L},{(-1L),1L,0L,3L},{(-1L),1L,1L,(-1L)}},{{0xE187876CL,3L,0xFB524446L,1L},{3L,1L,1L,(-3L)},{0x345A5EF8L,0xE187876CL,1L,(-3L)},{0xE2C58FA0L,1L,0xE2C58FA0L,1L},{(-1L),3L,(-2L),(-1L)},{0x345A5EF8L,1L,0xFB524446L,3L}},{{1L,1L,0xFB524446L,9L},{1L,1L,(-1L),0xB75A3807L},{0xFB524446L,0x1B2CCE87L,1L,0xE2C58FA0L},{1L,0xE2C58FA0L,0L,1L},{1L,0xE2C58FA0L,1L,0xE2C58FA0L},{0xE2C58FA0L,0x1B2CCE87L,9L,0xB75A3807L}},{{(-2L),1L,0L,9L},{0xFB524446L,0xE187876CL,(-3L),0xE2C58FA0L},{0xFB524446L,0L,0L,0xFB524446L},{(-2L),0xE2C58FA0L,9L,0L},{0xE2C58FA0L,0xE187876CL,1L,0xB75A3807L},{1L,(-2L),0L,0xB75A3807L}},{{1L,0xE187876CL,1L,0L},{0xFB524446L,0xE2C58FA0L,(-1L),0xFB524446L},{1L,0L,9L,0xE2C58FA0L},{0L,0xE187876CL,9L,9L},{1L,1L,(-1L),0xB75A3807L},{0xFB524446L,0x1B2CCE87L,1L,0xE2C58FA0L}},{{1L,0xE2C58FA0L,0L,1L},{1L,0xE2C58FA0L,1L,0xE2C58FA0L},{0xE2C58FA0L,0x1B2CCE87L,9L,0xB75A3807L},{(-2L),1L,0L,9L},{0xFB524446L,0xE187876CL,(-3L),0xE2C58FA0L},{0xFB524446L,0L,0L,0xFB524446L}}};
                        uint8_t l_876 = 0UL;
                        int i, j, k;
                        l_876--;
                        l_870.f3 ^= ((+((safe_rshift_func_int8_t_s_s(g_621[l_845][g_231][(l_845 + 2)], (g_26 = (safe_lshift_func_uint8_t_u_u((safe_mod_func_int32_t_s_s((l_867.f3 = (0xC4D5F2B8L <= ((safe_sub_func_int8_t_s_s(0L, (0x18475E14L <= 0xFD3A707DL))) < g_59[(l_845 + 7)]))), ((-1L) || l_507[l_847.f1]))), 7))))) || p_123)) || p_123);
                        return p_122;
                    }
                }

                g_152[0].f3 = (g_616[3] |= (p_123 = (safe_add_func_int8_t_s_s(((g_407 = (p_123 | (p_122 & g_23[2]))) | 0x4A959C6BL), ((((safe_mod_func_uint32_t_u_u((safe_rshift_func_uint8_t_u_s((safe_rshift_func_int8_t_s_u((safe_add_func_uint16_t_u_u(p_122, (safe_mul_func_uint8_t_u_u(((l_303 > (+(safe_lshift_func_int8_t_s_s(l_870.f1, 5)))) > ((!((0x7025L <= p_122) <= l_285.f1)) & 0x8E1DA620L)), p_123)))), p_122)), p_122)), g_80)) ^ (-6L)) < 0x5EL) & 0xF40BL)))));
            }
            l_507[0] ^= (safe_add_func_uint16_t_u_u((p_122 ^ (safe_lshift_func_int8_t_s_u((safe_mul_func_uint16_t_u_u((((safe_sub_func_int8_t_s_s(p_123, (+g_80))) | (safe_lshift_func_int8_t_s_s((l_867.f3 != (safe_mul_func_uint16_t_u_u(l_659, p_122))), (safe_add_func_int16_t_s_s(1L, (safe_sub_func_int32_t_s_s((~(((((l_622 = (((((p_123 || (g_59[7] ^= ((safe_sub_func_int32_t_s_s((safe_lshift_func_uint16_t_u_s((((g_81[2] > p_123) && p_122) ^ g_69), l_740)), p_123)) && l_624[6]))) < 0L) ^ 0UL) > g_4[7][0][1]) & p_122)) || p_123) <= g_3) | p_122) == p_122)), 0xD1E84D66L))))))) || 0L), g_26)), g_203[2]))), 0x3B67L));
        }
    }
    else
    {
        uint16_t l_970 = 0x9AC6L;
        int32_t l_980 = 1L;
        int32_t l_1022 = (-4L);
        uint32_t l_1077[7] = {0UL,0UL,0UL,0UL,0UL,0UL,0UL};
        int32_t l_1087 = 1L;
        int32_t l_1088 = 0xBDF36BE0L;
        int32_t l_1090 = 0x2795DD04L;
        int i;
        for (g_407 = 0; (g_407 != 15); g_407 = safe_add_func_uint8_t_u_u(g_407, 3))
        {
            uint32_t l_966 = 0xDD67FA6AL;
            uint32_t l_1023 = 8UL;
            int32_t l_1033 = 0x6DCB9A48L;
            int32_t l_1038[4] = {0L,0L,0L,0L};
            uint32_t l_1078 = 4294967290UL;
            int i;
            if ((safe_unary_minus_func_int16_t_s(g_58)))
            {
                uint32_t l_984 = 0xFE15CF8FL;
                for (l_345 = 23; (l_345 < (-24)); l_345 = safe_sub_func_uint32_t_u_u(l_345, 1))
                {
                    g_152[1] = g_152[0];
                }

                g_283.f3 = g_80;
                if ((p_123 ^= g_973))
                {
                    for (g_214 = 0; (g_214 <= 1); g_214 += 1)
                    {
                        g_58 |= p_123;
                        g_616[0] = (3UL || (safe_mod_func_uint8_t_u_u(l_866[0][2], g_976)));
                    }
                }
                else
                {
                    struct S0 l_987 = {-2L,-1L,0xAEB4F7DFL,1L,65531UL};
                    for (l_719 = (-24); (l_719 > (-28)); l_719--)
                    {
                        int8_t l_979 = 1L;
                        l_980 = l_979;

                        l_984--;
                        g_152[0] = l_987;
                    }
                    for (g_57 = 10; (g_57 == (-20)); g_57 = safe_sub_func_int16_t_s_s(g_57, 8))
                    {
                        l_987.f3 = 0x93FC31D0L;

                    }
                    g_283.f3 = (((l_987.f3 = ((((+1L) >= (((safe_lshift_func_int8_t_s_u((l_984 >= (((((safe_lshift_func_int8_t_s_u((0xEBF7868CL != (2L >= (0UL & (safe_mod_func_uint32_t_u_u(0UL, p_123))))), 7)) >= (safe_rshift_func_int8_t_s_u(((g_59[7] ^= (safe_sub_func_uint8_t_u_u((safe_rshift_func_uint16_t_u_u(g_4[4][2][1], (safe_add_func_uint8_t_u_u(3UL, 2UL)))), 0xBBL))) <= p_122), l_867.f3))) && l_980) & g_55[0][4]) || p_122)), l_1012)) | l_966) == l_980)) <= g_4[4][0][1]) <= p_123)) <= 0x00L) || g_277);
                }
            }
            else
            {
                int32_t l_1015 = 1L;
                int32_t l_1024 = 5L;

            }
            if ((p_123 = (+(safe_mod_func_uint8_t_u_u(((safe_mul_func_int16_t_s_s(((safe_rshift_func_int8_t_s_s(p_123, (safe_rshift_func_int8_t_s_s((0xAA9C0EEEL < ((g_551 = ((l_1033 = g_5[2]) & (g_22 |= ((safe_mul_func_uint32_t_u_u((g_621[0][2][4] > g_4[3][0][0]), (g_283.f3 <= (1UL >= (l_1038[1] &= ((safe_mul_func_uint8_t_u_u(l_1023, g_203[1])) > 4294967290UL)))))) ^ g_465)))) & 65535UL)), p_123)))) || l_369), g_152[0].f3)) >= 0x258E12C4L), l_970)))))
            {
                uint8_t l_1043 = 0x15L;
                l_347[5] = (safe_sub_func_int8_t_s_s((safe_lshift_func_int16_t_s_u((l_1043 > (p_123 ^ 0x483287C2L)), 7)), (((l_971 > ((((((safe_mod_func_uint32_t_u_u((safe_mod_func_uint16_t_u_u((p_122 = ((safe_mod_func_uint16_t_u_u((safe_mul_func_int16_t_s_s(((safe_rshift_func_int16_t_s_u((l_970 < (((safe_sub_func_uint32_t_u_u(((((safe_add_func_uint16_t_u_u(((safe_lshift_func_int8_t_s_s(l_866[1][4], 2)) && (safe_rshift_func_uint16_t_u_s((+((safe_unary_minus_func_int16_t_s((safe_sub_func_uint8_t_u_u((((+((safe_add_func_int16_t_s_s((safe_add_func_int32_t_s_s((safe_add_func_uint32_t_u_u((+(l_516 | (p_123 && (!(((safe_mod_func_uint16_t_u_u(((safe_rshift_func_uint16_t_u_u(l_1033, 7)) != g_283.f0), 3UL)) | l_1022) <= g_283.f4))))), 0x2B474F36L)), l_980)), 65535UL)) > p_123)) != 0x57L) != 0x45C0357EL), g_4[7][0][1])))) | g_277)), 2))), l_1033)) < 9UL) == l_970) | l_1077[3]), 0x8A13D2E9L)) || l_1022) == 1L)), p_122)) | p_123), g_234)), l_1078)) < 0L)), l_1022)), g_234)) == p_123) < l_1043) < l_1038[2]) && 1UL) < p_123)) ^ l_1038[1]) < l_980)));
            }
            else
            {
                int8_t l_1085[9];
                int32_t l_1086 = (-5L);
                int32_t l_1089[9];
                uint32_t l_1091 = 9UL;
                uint32_t l_1114 = 0x619A2BF8L;
                int i;
                for (i = 0; i < 9; i++)
                    l_1085[i] = (-1L);
                for (i = 0; i < 9; i++)
                    l_1089[i] = 0x671091CDL;
                for (l_1078 = 0; (l_1078 >= 53); l_1078 = safe_add_func_int32_t_s_s(l_1078, 4))
                {
                    l_1085[8] = (((safe_add_func_int32_t_s_s(0x43954A20L, (safe_rshift_func_int8_t_s_u(0x68L, 5)))) || 0xC254L) == (!l_966));
                    if (p_122)
                        break;
                }
                l_1091++;
                if (g_616[4])
                    break;
                p_123 = (safe_add_func_uint8_t_u_u((l_347[0] = ((p_123 ^ (safe_add_func_uint8_t_u_u((safe_mod_func_uint16_t_u_u((safe_lshift_func_int8_t_s_s(g_410, 6)), 1UL)), ((safe_lshift_func_uint8_t_u_s((g_466 & ((l_1114 = ((l_347[3] == (safe_mul_func_int16_t_s_s((((((l_1077[3] || (l_1089[7] ^= (g_152[0].f1 = (safe_add_func_uint8_t_u_u(((safe_mul_func_uint8_t_u_u((((l_1078 > ((0xB2F6L && (0x11L < p_123)) <= (-7L))) || l_624[6]) & g_55[6][6]), p_122)) || (-1L)), l_867.f2))))) < 0L) || 0x79D8L) && g_26) != p_122), g_5[2]))) > 4294967290UL)) >= p_122)), 3)) >= (-1L))))) && l_1033)), l_1085[8]));
            }
        }
    }
lbl_1848:
    if ((safe_div_func_int8_t_s_s((-5L), ((~(p_122 >= ((safe_add_func_int32_t_s_s((safe_add_func_int32_t_s_s((0xCCDFF050L || (0x58710855L <= (safe_lshift_func_uint16_t_u_s((safe_lshift_func_int8_t_s_s((-7L), 6)), (safe_rshift_func_uint16_t_u_s((p_123 || (g_152[0].f1 ^ ((l_1012 & g_57) != g_152[0].f3))), 12)))))), l_624[6])), 0xB3E01154L)) < p_123))) & l_1012))))
    {
        uint32_t l_1133[4];
        int32_t l_1146 = 1L;
        int32_t l_1149 = 2L;
        int i;
        for (i = 0; i < 4; i++)
            l_1133[i] = 1UL;

    }
    else
    {
        int16_t l_1150 = 0L;
        int32_t l_1171 = 0x5FCB9C23L;
        uint16_t l_1213 = 65535UL;
        struct S0 l_1259[6][7] = {{{0x41L,0x50L,0UL,0xC57CECDCL,1UL},{0x20L,-1L,0UL,0x3B02E1CAL,0x8C2BL},{7L,0L,0x0096F722L,0xD7996284L,4UL},{0x20L,-1L,0UL,0x3B02E1CAL,0x8C2BL},{0x41L,0x50L,0UL,0xC57CECDCL,1UL},{0xEFL,0x01L,4294967286UL,1L,0x636CL},{0xEFL,0x01L,4294967286UL,1L,0x636CL}},{{0L,0x64L,0xA32F95C5L,0xB91AD969L,65532UL},{0xE6L,0x45L,0x630E9ACBL,1L,0x581DL},{0x59L,0x71L,0UL,0x47246FAAL,65535UL},{0xE6L,0x45L,0x630E9ACBL,1L,0x581DL},{0L,0x64L,0xA32F95C5L,0xB91AD969L,65532UL},{-1L,0x8BL,0UL,1L,65531UL},{-1L,0x8BL,0UL,1L,65531UL}},{{0x41L,0x50L,0UL,0xC57CECDCL,1UL},{0x20L,-1L,0UL,0x3B02E1CAL,0x8C2BL},{7L,0L,0x0096F722L,0xD7996284L,4UL},{0x20L,-1L,0UL,0x3B02E1CAL,0x8C2BL},{0x41L,0x50L,0UL,0xC57CECDCL,1UL},{0xEFL,0x01L,4294967286UL,1L,0x636CL},{0xEFL,0x01L,4294967286UL,1L,0x636CL}},{{0L,0x64L,0xA32F95C5L,0xB91AD969L,65532UL},{0xE6L,0x45L,0x630E9ACBL,1L,0x581DL},{0x59L,0x71L,0UL,0x47246FAAL,65535UL},{0xE6L,0x45L,0x630E9ACBL,1L,0x581DL},{0L,0x64L,0xA32F95C5L,0xB91AD969L,65532UL},{-1L,0x8BL,0UL,1L,65531UL},{-1L,0x8BL,0UL,1L,65531UL}},{{0x41L,0x50L,0UL,0xC57CECDCL,1UL},{0x20L,-1L,0UL,0x3B02E1CAL,0x8C2BL},{7L,0L,0x0096F722L,0xD7996284L,4UL},{0x20L,-1L,0UL,0x3B02E1CAL,0x8C2BL},{0x41L,0x50L,0UL,0xC57CECDCL,1UL},{0xEFL,0x01L,4294967286UL,1L,0x636CL},{0xEFL,0x01L,4294967286UL,1L,0x636CL}},{{0L,0x64L,0xA32F95C5L,0xB91AD969L,65532UL},{0xE6L,0x45L,0x630E9ACBL,1L,0x581DL},{0x59L,0x71L,0UL,0x47246FAAL,65535UL},{0xE6L,0x45L,0x630E9ACBL,1L,0x581DL},{0L,0x64L,0xA32F95C5L,0xB91AD969L,65532UL},{-1L,0x8BL,0UL,1L,65531UL},{-1L,0x8BL,0UL,1L,65531UL}}};
        int32_t l_1535[1];
        uint32_t l_1772[2];
        uint8_t l_1807 = 0x6AL;
        int8_t l_1837 = (-6L);
        int i, j;
        for (i = 0; i < 1; i++)
            l_1535[i] = 0x87FCAC24L;
        for (i = 0; i < 2; i++)
            l_1772[i] = 0x42EDABADL;
        if (l_1150)
        {
            uint32_t l_1153[8];
            int32_t l_1202 = (-1L);
            struct S0 l_1260 = {0x69L,0x93L,0xD348E8FBL,0xD4B3D304L,0xCE2EL};
            int8_t l_1282 = 0xE0L;
            uint8_t l_1310 = 0x54L;
            int16_t l_1522[2][4] = {{0x2212L,0x5C13L,0x5C13L,0x2212L},{0x5C13L,0x2212L,0x5C13L,0x5C13L}};
            int32_t l_1529 = 1L;
            int32_t l_1530 = (-6L);
            int32_t l_1533[3];
            int8_t l_1591 = 0x67L;
            int i, j;
            for (i = 0; i < 8; i++)
                l_1153[i] = 0x0A49B1F4L;
            for (i = 0; i < 3; i++)
                l_1533[i] = 0x6234C40EL;
            if (((l_1171 |= ((~(4294967295UL < (safe_div_func_uint16_t_u_u((8UL ^ l_1153[5]), (-4L))))) ^ ((~(p_122 = (((safe_add_func_int8_t_s_s((((safe_rshift_func_int8_t_s_s(0xCDL, 0)) == (safe_lshift_func_int8_t_s_u(8L, 0))) >= (safe_mul_func_int16_t_s_s((safe_mul_func_uint16_t_u_u(p_123, (safe_add_func_int16_t_s_s((safe_unary_minus_func_uint8_t_u((l_304[8] < (safe_rshift_func_uint8_t_u_s(((safe_add_func_int32_t_s_s(l_1153[6], 9UL)) && 254UL), 6))))), 65535UL)))), 0x97A4L))), p_123)) >= p_123) < p_122))) ^ g_407))) | g_80))
            {
                int32_t l_1192 = 6L;
                int32_t l_1215[7];
                int i;
                for (i = 0; i < 7; i++)
                    l_1215[i] = 0xF775074FL;
                l_1172 = 0x6FB0663AL;

                return g_5[0];
            }
            else
            {
                uint32_t l_1319[8][5] = {{4294967288UL,9UL,4294967294UL,0x20132B30L,9UL},{0x7CAEA579L,4294967294UL,4294967294UL,0x7CAEA579L,0x20132B30L},{4294967295UL,0x7CAEA579L,0x1E17F072L,9UL,9UL},{4294967288UL,0x7CAEA579L,4294967295UL,0x2160C3CDL,4294967294UL},{4294967288UL,0x1E17F072L,0x2160C3CDL,4294967288UL,0x2160C3CDL},{4294967288UL,4294967288UL,9UL,4294967294UL,0x20132B30L},{4294967295UL,0x20132B30L,0x2160C3CDL,0x2160C3CDL,0x20132B30L},{0x20132B30L,0x1E17F072L,4294967295UL,0x20132B30L,0x2160C3CDL}};
                int i, j;
                if (l_1171)
                    goto lbl_1305;

                for (g_973 = (-17); (g_973 < (-19)); --g_973)
                {
                    if (g_277)
                        break;
                }
            }
            if ((safe_lshift_func_int8_t_s_s(7L, 5)))
            {
                uint16_t l_1357 = 65534UL;
                uint16_t l_1358 = 0x3E62L;
                int32_t l_1386 = 0x49509442L;
                int32_t l_1387 = 1L;
                uint8_t l_1465 = 0xABL;
                int32_t l_1531 = 0x7EF660FDL;
                int32_t l_1532 = 0x8850771DL;
                int32_t l_1534 = 0x05EF42CDL;
                int32_t l_1536 = 0xB2E1E7F3L;
                int32_t l_1537[9][10][1] = {{{(-1L)},{0x141CA804L},{0x9AFE9FD3L},{0xE6EFE778L},{(-1L)},{0x1315D7F1L},{0L},{(-7L)},{0x9AFE9FD3L},{0xEA4215CDL}},{{0xEA4215CDL},{0x9AFE9FD3L},{(-7L)},{0L},{0x1315D7F1L},{(-1L)},{0xE6EFE778L},{0x9AFE9FD3L},{0x141CA804L},{(-1L)}},{{0x9AFE9FD3L},{0x1095593EL},{(-1L)},{0x1315D7F1L},{(-1L)},{0x1095593EL},{0x9AFE9FD3L},{(-1L)},{0x141CA804L},{0x9AFE9FD3L}},{{0xE6EFE778L},{(-1L)},{0x1315D7F1L},{0L},{(-7L)},{0x9AFE9FD3L},{0xEA4215CDL},{0xEA4215CDL},{0x9AFE9FD3L},{(-7L)}},{{0L},{0x1315D7F1L},{(-1L)},{0xE6EFE778L},{0x9AFE9FD3L},{0x141CA804L},{(-1L)},{0x9AFE9FD3L},{0x1095593EL},{(-1L)}},{{0x1315D7F1L},{(-1L)},{0x1095593EL},{0x9AFE9FD3L},{(-1L)},{0x141CA804L},{0x9AFE9FD3L},{0xE6EFE778L},{(-1L)},{0x1315D7F1L}},{{0L},{(-7L)},{0x9AFE9FD3L},{0xEA4215CDL},{0xEA4215CDL},{0x9AFE9FD3L},{(-7L)},{0L},{0x1315D7F1L},{(-1L)}},{{0xE6EFE778L},{0x9AFE9FD3L},{0x141CA804L},{(-1L)},{0x9AFE9FD3L},{0x1095593EL},{(-1L)},{0x1315D7F1L},{(-1L)},{0x1095593EL}},{{0x9AFE9FD3L},{(-1L)},{0x141CA804L},{0x9AFE9FD3L},{0xE6EFE778L},{(-1L)},{0x1315D7F1L},{0L},{(-7L)},{0x9AFE9FD3L}}};
                int32_t l_1562 = (-5L);
                int i, j, k;

                g_152[0].f3 |= (safe_mul_func_int16_t_s_s((safe_lshift_func_int8_t_s_u((safe_rshift_func_int16_t_s_u(p_122, (((((safe_mul_func_uint8_t_u_u((((safe_sub_func_uint32_t_u_u(4294967294UL, (g_80 == (g_466 = (((0x3B01B5C7L || (safe_sub_func_uint8_t_u_u((safe_sub_func_int8_t_s_s(((g_22--) == (safe_lshift_func_int16_t_s_s((l_1171 = (g_277 = (l_867.f3 = (l_1522[0][3] || (safe_mul_func_int16_t_s_s((safe_div_func_uint16_t_u_u((safe_rshift_func_int8_t_s_s((((g_59[4]++) | (safe_mod_func_uint32_t_u_u((--g_407), (safe_mul_func_uint16_t_u_u(0x16B7L, (l_1310 != (l_1259[0][3].f3 |= (safe_lshift_func_int8_t_s_s(((safe_rshift_func_int16_t_s_u((safe_sub_func_uint32_t_u_u(((((safe_div_func_uint32_t_u_u((((safe_rshift_func_int8_t_s_s(((safe_mod_func_uint8_t_u_u((safe_sub_func_int32_t_s_s((g_283.f3 = (p_123 = p_122)), (safe_rshift_func_int8_t_s_u(p_122, 4)))), g_973)) <= l_1562), g_283.f4)) | 0x0656L) < g_277), g_621[0][2][4])) ^ 255UL) > 1L) >= 9L), p_122)), g_621[0][2][4])) | g_69), p_122))))))))) && g_976), l_1536)), (-1L))), g_1477)))))), 14))), p_122)), (-3L)))) <= l_1533[2]) && p_123))))) <= p_122) & 0xCCL), (-8L))) | g_27) ^ p_122) >= p_122) == p_122))), l_624[6])), p_122));
            }
            else
            {
                int8_t l_1569 = 0x0FL;
                for (l_1385 = 0; (l_1385 <= 1); l_1385 += 1)
                {
                    p_123 = (g_80 = (safe_add_func_int8_t_s_s((255UL > (safe_mul_func_uint16_t_u_u((~(p_122 = ((l_1569 |= (g_22--)) > (l_369 = (g_1570 = 7UL))))), (-1L)))), (0xD850A0C7L & g_23[2]))));
                }
                p_123 = g_410;
            }

            for (l_719 = 0; (l_719 >= (-30)); l_719--)
            {
                return l_1310;
            }
        }
        else
        {
            uint32_t l_1594 = 0x02A7447CL;
            int32_t l_1605 = 0L;
            int32_t l_1635 = (-1L);
            int32_t l_1638[10] = {0xDE8763D0L,0x01B8A0EAL,0x01B8A0EAL,0xDE8763D0L,(-1L),0xDE8763D0L,0x01B8A0EAL,0x01B8A0EAL,0xDE8763D0L,(-1L)};
            uint32_t l_1639 = 1UL;
            int i;
            g_152[0] = func_129(l_1594, l_867, p_122, p_122);


        }
        for (g_551 = (-17); (g_551 == (-4)); g_551 = safe_add_func_uint16_t_u_u(g_551, 3))
        {
            uint16_t l_1656[5][5] = {{0x0118L,0x0118L,0x0118L,0x0118L,0x0118L},{65527UL,65527UL,65527UL,65527UL,65527UL},{0x0118L,0x0118L,0x0118L,0x0118L,0x0118L},{65527UL,65527UL,65527UL,65527UL,65527UL},{0x0118L,0x0118L,0x0118L,0x0118L,0x0118L}};
            uint32_t l_1682 = 0xDD197F9AL;
            uint32_t l_1683 = 0xDA97E711L;
            int32_t l_1702[9][7][3] = {{{0xD5AA79A0L,5L,0x1E4F5194L},{(-4L),0x42D84184L,0L},{0xB89ECFEDL,(-5L),0xD5AA79A0L},{0xD5AA79A0L,0x7A4E9EB1L,0xF010A5DCL},{(-8L),0x63256600L,0x42B3D5D4L},{(-8L),1L,(-8L)},{0xD5AA79A0L,1L,(-1L)}},{{0xB89ECFEDL,0x1E00C7A1L,7L},{(-4L),0xF8D685BBL,5L},{0xD5AA79A0L,3L,0x49B42B8DL},{(-4L),0x95C948F2L,0x159F0684L},{0xB89ECFEDL,4L,0xFF94318DL},{0xD5AA79A0L,5L,0xFF41CF9EL},{(-8L),0x0844377DL,0xEE184E30L}},{{(-8L),0L,(-4L)},{0xD5AA79A0L,0xC33DFE7DL,1L},{0xB89ECFEDL,(-7L),0x7E067FA1L},{(-4L),0L,0xA18595CBL},{0xD5AA79A0L,0x92C27E1EL,0L},{(-4L),0x40506DEFL,0xA971A149L},{0xB89ECFEDL,1L,0xBBECE0B6L}},{{0xD5AA79A0L,0L,(-7L)},{(-8L),(-1L),0x03373726L},{(-8L),0xC347CA7CL,0xB89ECFEDL},{0xD5AA79A0L,0x0E8B342DL,0x8911F421L},{0xB89ECFEDL,0x31D3D160L,1L},{(-4L),0xF844D560L,0xA6D10BCCL},{0xD5AA79A0L,5L,0x1E4F5194L}},{{(-4L),0x42D84184L,0L},{0xB89ECFEDL,(-5L),0xD5AA79A0L},{0xD5AA79A0L,0x7A4E9EB1L,0xF010A5DCL},{(-8L),0x63256600L,0x42B3D5D4L},{(-8L),1L,(-8L)},{0xD5AA79A0L,1L,(-1L)},{0xB89ECFEDL,0x1E00C7A1L,7L}},{{(-4L),0xF8D685BBL,5L},{0xD5AA79A0L,3L,0x49B42B8DL},{(-4L),0x95C948F2L,0x159F0684L},{0xB89ECFEDL,4L,0xFF94318DL},{0xD5AA79A0L,5L,0xFF41CF9EL},{(-8L),0x0844377DL,0xEE184E30L},{(-8L),0L,(-4L)}},{{0xD5AA79A0L,0xC33DFE7DL,1L},{0xB89ECFEDL,(-7L),0x7E067FA1L},{(-4L),0L,0xA18595CBL},{0xD5AA79A0L,0x92C27E1EL,0L},{(-4L),0x40506DEFL,0xA971A149L},{0xB89ECFEDL,1L,0xBBECE0B6L},{0xD5AA79A0L,0L,(-7L)}},{{(-8L),(-1L),0x03373726L},{(-8L),0xC347CA7CL,0xB89ECFEDL},{0xD5AA79A0L,0x0E8B342DL,0x8911F421L},{0xB89ECFEDL,0x31D3D160L,1L},{(-4L),0xF844D560L,0xA6D10BCCL},{0xD5AA79A0L,5L,0x1E4F5194L},{(-4L),0x42D84184L,0L}},{{0xB89ECFEDL,(-5L),0xD5AA79A0L},{0xD5AA79A0L,0x7A4E9EB1L,3L},{0xCE0DE4C5L,0x7E067FA1L,(-7L)},{0xCE0DE4C5L,(-1L),0xCE0DE4C5L},{(-1L),0xB89ECFEDL,(-3L)},{(-9L),0xEE184E30L,0L},{0x3DB16356L,0xF010A5DCL,0x2A3503FCL}}};
            uint32_t l_1714 = 4294967293UL;
            int32_t l_1752 = (-9L);
            int32_t l_1753 = 0xC1B6B7D7L;
            int8_t l_1792 = (-3L);
            int16_t l_1802[8] = {0x2823L,0xF365L,0x2823L,0x2823L,0xF365L,0x2823L,0x2823L,0xF365L};
            int32_t l_1836 = (-10L);
            int i, j, k;
            if (((safe_div_func_uint32_t_u_u(((safe_lshift_func_int8_t_s_s((safe_lshift_func_int16_t_s_u((((((((-5L) ^ 4UL) >= (safe_sub_func_uint32_t_u_u(p_123, (safe_mod_func_int16_t_s_s((safe_rshift_func_uint16_t_u_u(65535UL, (g_32 = 65530UL))), g_27))))) < l_1656[4][0]) <= (safe_div_func_int8_t_s_s((((g_59[7] >= (safe_sub_func_int16_t_s_s((l_1259[0][3].f3 == 9UL), l_1259[0][3].f0))) < l_1213) || g_973), p_122))) >= p_123) || l_1535[0]), 1)), l_1259[0][3].f4)) >= (-1L)), g_616[4])) || p_122))
            {
                uint16_t l_1679 = 0x0612L;
                g_283.f3 = 0x08965384L;
                for (l_292 = 0; (l_292 != (-22)); l_292--)
                {
                    return g_283.f4;
                }
                l_1172 = (p_123 ^= 0x900E2E27L);

            }
            else
            {
                uint8_t l_1699 = 0x76L;
                int32_t l_1703[6][3] = {{0x0FF7A101L,0L,0L},{(-10L),0xFFD1B46BL,0xFFD1B46BL},{0x0FF7A101L,0L,0L},{(-10L),0xFFD1B46BL,0xFFD1B46BL},{0x0FF7A101L,0L,0L},{(-10L),0xFFD1B46BL,0xFFD1B46BL}};
                int i, j;

                l_1704--;
                if (g_973)
                    goto lbl_1305;
                g_1707++;
            }
            for (l_1359 = (-4); (l_1359 >= 6); l_1359 = safe_add_func_uint16_t_u_u(l_1359, 3))
            {
                uint32_t l_1751[7][1][6] = {{{0x17E2ECABL,0x4E74212CL,0x4E74212CL,0x17E2ECABL,0xCC6F738EL,0xD22C8E63L}},{{0x17E2ECABL,0xCC6F738EL,0xD22C8E63L,4294967295UL,0x4E74212CL,0xD22C8E63L}},{{0x5CD62D2AL,1UL,0x4E74212CL,0x64719BFFL,0x4E74212CL,1UL}},{{4294967295UL,0xCC6F738EL,4294967295UL,0x64719BFFL,0xCC6F738EL,0x4E74212CL}},{{0x5CD62D2AL,0x4E74212CL,4294967295UL,4294967295UL,1UL,1UL}},{{0x17E2ECABL,0x4E74212CL,0x4E74212CL,0x17E2ECABL,0xCC6F738EL,0xD22C8E63L}},{{0x17E2ECABL,0xCC6F738EL,0xD22C8E63L,4294967295UL,0x4E74212CL,0xD22C8E63L}}};
                uint32_t l_1768 = 4294967293UL;
                struct S0 l_1770 = {0xCEL,-1L,0x16C4C5FAL,0xD85C1220L,0x4934L};
                int32_t l_1775 = 0x81B8E7BBL;
                int i, j, k;

            }
            for (l_1682 = 0; (l_1682 <= 4); l_1682 += 1)
            {
                int32_t l_1793 = (-7L);
                int32_t l_1794 = 1L;
                int32_t l_1795 = 0x75322655L;
                int32_t l_1796 = (-5L);
                int32_t l_1797 = 0x3CD94247L;
                int32_t l_1798 = (-1L);
                int32_t l_1799 = 0x4E890445L;
                int32_t l_1800 = 8L;
                int32_t l_1803 = 7L;
                int32_t l_1804 = 7L;
                int32_t l_1805 = 1L;
                int32_t l_1806[2];
                int i, j;
                for (i = 0; i < 2; i++)
                    l_1806[i] = 0xA361129CL;
                if (l_1656[l_1682][l_1682])
                    break;
                l_1807--;
            }

        }
    }










    return g_1707;
}







static uint16_t func_124(struct S0 p_125, struct S0 p_126, struct S0 p_127, int32_t p_128)
{


{
    for (g_58 = 0; g_58 < 9; g_58 += 1)
    {
        g_59[g_58] = 0UL;
    }
    return g_57;
}


    return g_57;
}







static struct S0 func_129(int32_t p_130, struct S0 p_131, uint32_t p_132, int16_t p_133)
{
    struct S0 l_151 = {0x15L,-5L,0UL,1L,0xBB46L};
    int32_t l_195 = 0x2C72D125L;
    int16_t l_230 = 1L;
    uint32_t l_235 = 4294967295UL;
    uint16_t l_280 = 0xE747L;


for (p_132 = 0; (p_132 <= 39); ++p_132)
    {
        int32_t l_164 = (-2L);
        int32_t l_199 = 1L;
        int32_t l_276 = 8L;
        for (p_131.f0 = 0; (p_131.f0 <= 2); p_131.f0 += 1)
        {
            int8_t l_163[9][6] = {{0x75L,0x92L,0x92L,0x75L,0xC2L,(-7L)},{(-7L),0x75L,6L,0x75L,(-7L),1L},{0x75L,(-7L),1L,1L,(-7L),0x75L},{0x92L,0x75L,0xC2L,(-7L),0xC2L,0x75L},{0xC2L,0x92L,1L,6L,6L,1L},{0xC2L,0xC2L,6L,(-7L),0x46L,(-7L)},{0x92L,0xC2L,0x92L,1L,6L,6L},{0x75L,0x92L,0x92L,0x75L,0xC2L,(-7L)},{(-7L),0x75L,6L,0x75L,(-7L),1L}};
            uint32_t l_165 = 0x1019322EL;
            struct S0 l_166 = {0L,0L,4UL,0L,0x9C02L};
            int32_t l_197 = 9L;
            int32_t l_200 = 0x027B00CAL;
            uint32_t l_224 = 9UL;
            int8_t l_279 = (-1L);
            int i, j;
            g_152[0] = l_151;
            l_151.f3 = g_81[p_131.f0];
            if (((g_23[p_131.f0] < (safe_lshift_func_int16_t_s_u((((l_151.f0 ^ (safe_mod_func_int16_t_s_s(0x58C3L, (safe_sub_func_uint8_t_u_u((((safe_lshift_func_int8_t_s_u(p_132, (--g_22))) <= 4UL) && (p_131.f4 = 0x517BL)), 8UL))))) & (l_164 = l_163[1][3])) | p_133), 12))) ^ l_151.f1))
            {
                struct S0 l_196 = {1L,0x8BL,0x6BBBDF83L,5L,0xEF4FL};
                int32_t l_202 = 0xD4C5443CL;
                if ((!g_152[0].f0))
                {
                    g_152[0] = g_152[1];
                }
                else
                {
                    uint32_t l_177 = 0xAEAE63DAL;
                    uint16_t l_194 = 65535UL;
                    int32_t l_198 = 0x43B8F344L;
                    l_165 = p_130;
                    l_166 = g_152[0];
                    g_80 = (+((safe_mul_func_int16_t_s_s(((((l_164 ^ ((g_58 | ((safe_sub_func_uint8_t_u_u((safe_mod_func_int16_t_s_s(((safe_rshift_func_uint16_t_u_u((l_151.f3 ^= g_4[7][0][1]), ((l_177 != (g_57 == (((safe_add_func_uint8_t_u_u((safe_unary_minus_func_uint32_t_u((safe_sub_func_uint32_t_u_u(g_4[7][0][1], (safe_unary_minus_func_int8_t_s(((l_195 = (safe_mul_func_int16_t_s_s((((((safe_lshift_func_uint8_t_u_s((safe_mod_func_int32_t_s_s((g_152[0].f3 |= (safe_add_func_uint16_t_u_u((safe_div_func_uint16_t_u_u(((((p_133 = 0x557EL) < 0L) & 0x264C02D8L) ^ 1L), l_194)), g_32))), 0xBCA6F5D4L)), 2)) && 0xC7L) && 0xC0AAL) && p_131.f1) | g_23[1]), g_152[0].f4))) != g_23[2]))))))), g_5[2])) || 255UL) | 1UL))) > g_152[0].f0))) && 0L), l_151.f0)), g_57)) == 0xF4L)) < 0x12L)) ^ g_57) <= l_166.f2) == (-10L)), (-1L))) < p_131.f1));
                    for (l_164 = 0; (l_164 <= 2); l_164 += 1)
                    {
                        int16_t l_201 = 1L;
                        g_152[0] = l_196;
                        l_197 &= (8L | p_130);
                        g_203[2]++;
                    }
                }

            }
            else
            {
                uint16_t l_225[8];
                int i;
                for (i = 0; i < 8; i++)
                    l_225[i] = 0x7036L;
                l_225[5]++;
                for (l_200 = 0; (l_200 <= 2); l_200 += 1)
                {
                    int32_t l_228[3];
                    int32_t l_229[4] = {0x011ED2F5L,0x011ED2F5L,0x011ED2F5L,0x011ED2F5L};
                    int i;
                    for (i = 0; i < 3; i++)
                        l_228[i] = 0x4E14C23FL;
                    for (g_32 = 3; (g_32 <= 8); g_32 += 1)
                    {
                        int32_t l_278[6] = {7L,7L,7L,7L,7L,7L};
                        int i;
                        --g_231;
                        l_235++;

                        l_278[0] |= 5L;
                    }
                    l_151 = g_152[1];
                }
                l_279 = g_81[2];
            }
        }
    }


    for (l_195 = 0; (l_195 <= 3); l_195 += 1)
    {
        int i;
        if (g_81[l_195])
            break;


for (p_132 = 0; (p_132 <= 39); ++p_132)
    {
        int32_t l_164 = (-2L);
        int32_t l_199 = 1L;
        int32_t l_276 = 8L;
        for (p_131.f0 = 0; (p_131.f0 <= 2); p_131.f0 += 1)
        {
            int8_t l_163[9][6] = {{0x75L,0x92L,0x92L,0x75L,0xC2L,(-7L)},{(-7L),0x75L,6L,0x75L,(-7L),1L},{0x75L,(-7L),1L,1L,(-7L),0x75L},{0x92L,0x75L,0xC2L,(-7L),0xC2L,0x75L},{0xC2L,0x92L,1L,6L,6L,1L},{0xC2L,0xC2L,6L,(-7L),0x46L,(-7L)},{0x92L,0xC2L,0x92L,1L,6L,6L},{0x75L,0x92L,0x92L,0x75L,0xC2L,(-7L)},{(-7L),0x75L,6L,0x75L,(-7L),1L}};
            uint32_t l_165 = 0x1019322EL;
            struct S0 l_166 = {0L,0L,4UL,0L,0x9C02L};
            int32_t l_197 = 9L;
            int32_t l_200 = 0x027B00CAL;
            uint32_t l_224 = 9UL;
            int8_t l_279 = (-1L);
            int i, j;
            g_152[0] = l_151;
            l_151.f3 = g_81[p_131.f0];
            if (((g_23[p_131.f0] < (safe_lshift_func_int16_t_s_u((((l_151.f0 ^ (safe_mod_func_int16_t_s_s(0x58C3L, (safe_sub_func_uint8_t_u_u((((safe_lshift_func_int8_t_s_u(p_132, (--g_22))) <= 4UL) && (p_131.f4 = 0x517BL)), 8UL))))) & (l_164 = l_163[1][3])) | p_133), 12))) ^ l_151.f1))
            {
                struct S0 l_196 = {1L,0x8BL,0x6BBBDF83L,5L,0xEF4FL};
                int32_t l_202 = 0xD4C5443CL;
                if ((!g_152[0].f0))
                {
                    g_152[0] = g_152[1];
                }
                else
                {
                    uint32_t l_177 = 0xAEAE63DAL;
                    uint16_t l_194 = 65535UL;
                    int32_t l_198 = 0x43B8F344L;
                    l_165 = p_130;
                    l_166 = g_152[0];
                    g_80 = (+((safe_mul_func_int16_t_s_s(((((l_164 ^ ((g_58 | ((safe_sub_func_uint8_t_u_u((safe_mod_func_int16_t_s_s(((safe_rshift_func_uint16_t_u_u((l_151.f3 ^= g_4[7][0][1]), ((l_177 != (g_57 == (((safe_add_func_uint8_t_u_u((safe_unary_minus_func_uint32_t_u((safe_sub_func_uint32_t_u_u(g_4[7][0][1], (safe_unary_minus_func_int8_t_s(((l_195 = (safe_mul_func_int16_t_s_s((((((safe_lshift_func_uint8_t_u_s((safe_mod_func_int32_t_s_s((g_152[0].f3 |= (safe_add_func_uint16_t_u_u((safe_div_func_uint16_t_u_u(((((p_133 = 0x557EL) < 0L) & 0x264C02D8L) ^ 1L), l_194)), g_32))), 0xBCA6F5D4L)), 2)) && 0xC7L) && 0xC0AAL) && p_131.f1) | g_23[1]), g_152[0].f4))) != g_23[2]))))))), g_5[2])) || 255UL) | 1UL))) > g_152[0].f0))) && 0L), l_151.f0)), g_57)) == 0xF4L)) < 0x12L)) ^ g_57) <= l_166.f2) == (-10L)), (-1L))) < p_131.f1));
                    for (l_164 = 0; (l_164 <= 2); l_164 += 1)
                    {
                        int16_t l_201 = 1L;
                        g_152[0] = l_196;
                        l_197 &= (8L | p_130);
                        g_203[2]++;
                    }
                }

            }
            else
            {
                uint16_t l_225[8];
                int i;
                for (i = 0; i < 8; i++)
                    l_225[i] = 0x7036L;
                l_225[5]++;
                for (l_200 = 0; (l_200 <= 2); l_200 += 1)
                {
                    int32_t l_228[3];
                    int32_t l_229[4] = {0x011ED2F5L,0x011ED2F5L,0x011ED2F5L,0x011ED2F5L};
                    int i;
                    for (i = 0; i < 3; i++)
                        l_228[i] = 0x4E14C23FL;
                    for (g_32 = 3; (g_32 <= 8); g_32 += 1)
                    {
                        int32_t l_278[6] = {7L,7L,7L,7L,7L,7L};
                        int i;
                        --g_231;
                        l_235++;

                        l_278[0] |= 5L;
                    }
                    l_151 = g_152[1];
                }
                l_279 = g_81[2];
            }
        }
    }


    }
for (p_132 = 0; (p_132 <= 39); ++p_132)
    {
        int32_t l_164 = (-2L);
        int32_t l_199 = 1L;
        int32_t l_276 = 8L;
        for (p_131.f0 = 0; (p_131.f0 <= 2); p_131.f0 += 1)
        {
            int8_t l_163[9][6] = {{0x75L,0x92L,0x92L,0x75L,0xC2L,(-7L)},{(-7L),0x75L,6L,0x75L,(-7L),1L},{0x75L,(-7L),1L,1L,(-7L),0x75L},{0x92L,0x75L,0xC2L,(-7L),0xC2L,0x75L},{0xC2L,0x92L,1L,6L,6L,1L},{0xC2L,0xC2L,6L,(-7L),0x46L,(-7L)},{0x92L,0xC2L,0x92L,1L,6L,6L},{0x75L,0x92L,0x92L,0x75L,0xC2L,(-7L)},{(-7L),0x75L,6L,0x75L,(-7L),1L}};
            uint32_t l_165 = 0x1019322EL;
            struct S0 l_166 = {0L,0L,4UL,0L,0x9C02L};
            int32_t l_197 = 9L;
            int32_t l_200 = 0x027B00CAL;
            uint32_t l_224 = 9UL;
            int8_t l_279 = (-1L);
            int i, j;
            g_152[0] = l_151;
            l_151.f3 = g_81[p_131.f0];
            if (((g_23[p_131.f0] < (safe_lshift_func_int16_t_s_u((((l_151.f0 ^ (safe_mod_func_int16_t_s_s(0x58C3L, (safe_sub_func_uint8_t_u_u((((safe_lshift_func_int8_t_s_u(p_132, (--g_22))) <= 4UL) && (p_131.f4 = 0x517BL)), 8UL))))) & (l_164 = l_163[1][3])) | p_133), 12))) ^ l_151.f1))
            {
                struct S0 l_196 = {1L,0x8BL,0x6BBBDF83L,5L,0xEF4FL};
                int32_t l_202 = 0xD4C5443CL;
                if ((!g_152[0].f0))
                {
                    g_152[0] = g_152[1];
                }
                else
                {
                    uint32_t l_177 = 0xAEAE63DAL;
                    uint16_t l_194 = 65535UL;
                    int32_t l_198 = 0x43B8F344L;
                    l_165 = p_130;
                    l_166 = g_152[0];
                    g_80 = (+((safe_mul_func_int16_t_s_s(((((l_164 ^ ((g_58 | ((safe_sub_func_uint8_t_u_u((safe_mod_func_int16_t_s_s(((safe_rshift_func_uint16_t_u_u((l_151.f3 ^= g_4[7][0][1]), ((l_177 != (g_57 == (((safe_add_func_uint8_t_u_u((safe_unary_minus_func_uint32_t_u((safe_sub_func_uint32_t_u_u(g_4[7][0][1], (safe_unary_minus_func_int8_t_s(((l_195 = (safe_mul_func_int16_t_s_s((((((safe_lshift_func_uint8_t_u_s((safe_mod_func_int32_t_s_s((g_152[0].f3 |= (safe_add_func_uint16_t_u_u((safe_div_func_uint16_t_u_u(((((p_133 = 0x557EL) < 0L) & 0x264C02D8L) ^ 1L), l_194)), g_32))), 0xBCA6F5D4L)), 2)) && 0xC7L) && 0xC0AAL) && p_131.f1) | g_23[1]), g_152[0].f4))) != g_23[2]))))))), g_5[2])) || 255UL) | 1UL))) > g_152[0].f0))) && 0L), l_151.f0)), g_57)) == 0xF4L)) < 0x12L)) ^ g_57) <= l_166.f2) == (-10L)), (-1L))) < p_131.f1));
                    for (l_164 = 0; (l_164 <= 2); l_164 += 1)
                    {
                        int16_t l_201 = 1L;
                        g_152[0] = l_196;
                        l_197 &= (8L | p_130);
                        g_203[2]++;
                    }
                }

            }
            else
            {
                uint16_t l_225[8];
                int i;
                for (i = 0; i < 8; i++)
                    l_225[i] = 0x7036L;
                l_225[5]++;
                for (l_200 = 0; (l_200 <= 2); l_200 += 1)
                {
                    int32_t l_228[3];
                    int32_t l_229[4] = {0x011ED2F5L,0x011ED2F5L,0x011ED2F5L,0x011ED2F5L};
                    int i;
                    for (i = 0; i < 3; i++)
                        l_228[i] = 0x4E14C23FL;
                    for (g_32 = 3; (g_32 <= 8); g_32 += 1)
                    {
                        int32_t l_278[6] = {7L,7L,7L,7L,7L,7L};
                        int i;
                        --g_231;
                        l_235++;

                        l_278[0] |= 5L;
                    }
                    l_151 = g_152[1];
                }
                l_279 = g_81[2];
            }
        }
    }



    --l_280;
--l_280;



    return p_131;
}





int main (int argc, char* argv[])
{
    int i, j, k;
    int print_hash_value = 0;

    func_1();
    transparent_crc(g_3, "g_3", print_hash_value);
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j < 4; j++)
        {
            for (k = 0; k < 2; k++)
            {
                transparent_crc(g_4[i][j][k], "g_4[i][j][k]", print_hash_value);
                if (print_hash_value) printf("index = [%d][%d][%d]\n", i, j, k);

            }
        }
    }
    for (i = 0; i < 3; i++)
    {
        transparent_crc(g_5[i], "g_5[i]", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    transparent_crc(g_22, "g_22", print_hash_value);
    for (i = 0; i < 3; i++)
    {
        transparent_crc(g_23[i], "g_23[i]", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    transparent_crc(g_26, "g_26", print_hash_value);
    transparent_crc(g_27, "g_27", print_hash_value);
    transparent_crc(g_32, "g_32", print_hash_value);
    for (i = 0; i < 9; i++)
    {
        for (j = 0; j < 8; j++)
        {
            transparent_crc(g_55[i][j], "g_55[i][j]", print_hash_value);
            if (print_hash_value) printf("index = [%d][%d]\n", i, j);

        }
    }
    transparent_crc(g_57, "g_57", print_hash_value);
    transparent_crc(g_58, "g_58", print_hash_value);
    for (i = 0; i < 9; i++)
    {
        transparent_crc(g_59[i], "g_59[i]", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    transparent_crc(g_69, "g_69", print_hash_value);
    transparent_crc(g_80, "g_80", print_hash_value);
    for (i = 0; i < 4; i++)
    {
        transparent_crc(g_81[i], "g_81[i]", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    for (i = 0; i < 2; i++)
    {
        transparent_crc(g_152[i].f0, "g_152[i].f0", print_hash_value);
        transparent_crc(g_152[i].f1, "g_152[i].f1", print_hash_value);
        transparent_crc(g_152[i].f2, "g_152[i].f2", print_hash_value);
        transparent_crc(g_152[i].f3, "g_152[i].f3", print_hash_value);
        transparent_crc(g_152[i].f4, "g_152[i].f4", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    for (i = 0; i < 3; i++)
    {
        transparent_crc(g_203[i], "g_203[i]", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    transparent_crc(g_214, "g_214", print_hash_value);
    transparent_crc(g_231, "g_231", print_hash_value);
    transparent_crc(g_234, "g_234", print_hash_value);
    transparent_crc(g_277, "g_277", print_hash_value);
    transparent_crc(g_283.f0, "g_283.f0", print_hash_value);
    transparent_crc(g_283.f1, "g_283.f1", print_hash_value);
    transparent_crc(g_283.f2, "g_283.f2", print_hash_value);
    transparent_crc(g_283.f3, "g_283.f3", print_hash_value);
    transparent_crc(g_283.f4, "g_283.f4", print_hash_value);
    transparent_crc(g_407, "g_407", print_hash_value);
    transparent_crc(g_410, "g_410", print_hash_value);
    transparent_crc(g_465, "g_465", print_hash_value);
    transparent_crc(g_466, "g_466", print_hash_value);
    transparent_crc(g_551, "g_551", print_hash_value);
    for (i = 0; i < 5; i++)
    {
        transparent_crc(g_616[i], "g_616[i]", print_hash_value);
        if (print_hash_value) printf("index = [%d]\n", i);

    }
    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < 9; j++)
        {
            for (k = 0; k < 5; k++)
            {
                transparent_crc(g_621[i][j][k], "g_621[i][j][k]", print_hash_value);
                if (print_hash_value) printf("index = [%d][%d][%d]\n", i, j, k);

            }
        }
    }
    transparent_crc(g_973, "g_973", print_hash_value);
    transparent_crc(g_976, "g_976", print_hash_value);
    transparent_crc(g_1185, "g_1185", print_hash_value);
    transparent_crc(g_1356, "g_1356", print_hash_value);
    transparent_crc(g_1477, "g_1477", print_hash_value);
    transparent_crc(g_1570, "g_1570", print_hash_value);
    transparent_crc(g_1707, "g_1707", print_hash_value);
    transparent_crc(g_1917, "g_1917", print_hash_value);
    transparent_crc(g_2181, "g_2181", print_hash_value);
    transparent_crc(g_2432, "g_2432", print_hash_value);

    return 0;
}
