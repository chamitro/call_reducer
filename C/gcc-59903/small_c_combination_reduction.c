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
(safe_mul_func_int8_t_s_s)(int8_t si1, int8_t si2 )
{
  return
    si1 * si2;
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
(safe_add_func_int32_t_s_s)(int32_t si1, int32_t si2 )
{
  return
    (((si1>0) && (si2>0) && (si1 > ((2147483647)-si2))) || ((si1<0) && (si2<0) && (si1 < ((-2147483647-1)-si2)))) ?
    ((si1)) :
    (si1 + si2);
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
(safe_lshift_func_uint8_t_u_s)(uint8_t left, int right )
{
  return
    ((((int)right) < 0) || (((int)right) >= 32) || (left > ((255) >> ((int)right)))) ?
    ((left)) :
    (left << ((int)right));
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
(safe_sub_func_uint32_t_u_u)(uint32_t ui1, uint32_t ui2 )
{
  return ui1 - ui2;
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
static int32_t g_80 = 0xD47B9DA0L;
static uint32_t g_81[4] = {0xFACDC9FFL,0xFACDC9FFL,0xFACDC9FFL,0xFACDC9FFL};
static struct S0 g_152[2] = {{0x6EL,1L,0UL,0x4AB730D5L,0UL},{0x6EL,1L,0UL,0x4AB730D5L,0UL}};
static uint16_t g_203[3] = {0x582DL,0x582DL,0x582DL};
static int16_t g_277 = 1L;
static struct S0 g_283 = {0xB0L,-1L,0xF2B8033DL,0x5451DF1BL,0x022DL};
static int32_t g_410 = 0x38F403BAL;
static int32_t g_616[5] = {0x79C30704L,0x79C30704L,0x79C30704L,0x79C30704L,0x79C30704L};
static int32_t g_621[2][9][5] = {{{(-10L),1L,0xD5EF2F06L,1L,(-10L)},{1L,1L,8L,(-10L),8L},{8L,8L,0xD5EF2F06L,(-10L),0x1E4228D9L},{1L,1L,1L,1L,8L},{1L,(-10L),(-4L),(-4L),(-10L)},{8L,1L,(-4L),0xD5EF2F06L,0xD5EF2F06L},{1L,8L,1L,(-4L),0xD5EF2F06L},{(-10L),1L,0xD5EF2F06L,1L,(-10L)},{1L,1L,8L,(-10L),8L}},{{8L,8L,0xD5EF2F06L,(-10L),0x1E4228D9L},{1L,1L,1L,1L,8L},{1L,(-4L),0xD5EF2F06L,0xD5EF2F06L,(-4L)},{0x1E4228D9L,(-10L),0xD5EF2F06L,8L,8L},{(-10L),0x1E4228D9L,(-10L),0xD5EF2F06L,8L},{(-4L),1L,8L,1L,(-4L)},{(-10L),1L,0x1E4228D9L,(-4L),0x1E4228D9L},{0x1E4228D9L,0x1E4228D9L,8L,(-4L),1L},{1L,(-10L),(-10L),1L,0x1E4228D9L}}};
static uint32_t g_1707 = 5UL;
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
                }
{
                uint32_t l_35 = 6UL;
                int32_t l_2513 = (-1L);
                int8_t l_2552 = 4L;
                struct S0 l_2555 = {5L,-4L,4294967287UL,0xA1966BB6L,0x5237L};
                int i, j;
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
                }
                else
                {
                    uint16_t l_2551 = 0x102DL;
                    return g_152[0];
                }
                g_152[0] = g_283;
            }
            }
            if (((safe_mod_func_uint16_t_u_u((~(g_152[0].f4 >= ((5L != g_283.f1) != (l_33 = 0x57L)))), (g_1707 && 0xDEADU))) < ((0x1A0B5C90L > l_2620) ^ l_2550)))
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
                g_152[0] = g_283;
            }
            if (((safe_mod_func_uint16_t_u_u((~(g_152[0].f4 >= ((5L != g_283.f1) != (l_33 = 0x57L)))), (g_1707 && 0xDEADU))) < ((0x1A0B5C90L > l_2620) ^ l_2550)))
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
                l_2667[6] ^= ((safe_add_func_int16_t_s_s(((5L & (safe_add_func_int8_t_s_s((l_2550 <= (g_283.f1 = (safe_add_func_int32_t_s_s((g_410 = (~((l_2649 = l_2556.f0) <= (((l_34 = (safe_mul_func_int8_t_s_s((safe_lshift_func_uint16_t_u_s((0xDEADU != ((0xCC5416E9L >= ((l_2666 |= (safe_rshift_func_uint16_t_u_s(((((l_2665 |= (safe_mod_func_int8_t_s_s((1UL <= 0xDEADBEEFU), (safe_sub_func_uint8_t_u_u((((safe_rshift_func_int16_t_s_s((((0xB108ADECL == (0xFBCAL < l_33)) != g_283.f1) & l_2549), l_56[1][0][1])) && g_3) ^ l_56[0][1][0]), l_2664))))) < l_2664) || 0xD27E149AL) >= l_63), l_2[9][0]))) != 0x3934D295L)) < 0L)), 12)), g_27))) <= 0x3C2BL) && 0xDEADBEEF)))), l_2556.f1)))), g_5[1]))) < l_2642[3][2][1]), g_277)) < l_2556.f1);
                if (l_30)
                    continue;
                for (g_283.f3 = 22; (g_283.f3 <= 26); g_283.f3 = safe_add_func_int16_t_s_s(g_283.f3, 7))
                {
                    uint32_t l_2717 = 4294967287UL;
                    int32_t l_2751 = 0x0816A1D2L;
                    int32_t l_2765 = 0x6072443AL;
                    uint8_t l_2785 = 255UL;
                    l_2717++;
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
            return 0xDEADBEEF;
        }
    }
for (i = 0; i < 6; i++)
        l_145[i] = 0xE41B645FL;
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
            return 0xDEADBEEF;
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
lbl_1848:
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
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j < 4; j++)
        {
            for (k = 0; k < 2; k++)
            {
                if (print_hash_value) printf("index = [%d][%d][%d]\n", i, j, k);
            }
        }
    }
    for (i = 0; i < 3; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 3; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 9; i++)
    {
        for (j = 0; j < 8; j++)
        {
            if (print_hash_value) printf("index = [%d][%d]\n", i, j);
        }
    }
    for (i = 0; i < 9; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 4; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 2; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 3; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 5; i++)
    {
        if (print_hash_value) printf("index = [%d]\n", i);
    }
    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < 9; j++)
        {
            for (k = 0; k < 5; k++)
            {
                if (print_hash_value) printf("index = [%d][%d][%d]\n", i, j, k);
            }
        }
    }
    return 0;
}