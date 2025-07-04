#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

// Removal function
static int16_t
(safe_lshift_func_int16_t_s_s)(int16_t left, int right )
{

  return

    ((left < 0) || (((int)right) < 0) || (((int)right) >= 32) || (left > ((32767) >> ((int)right)))) ?
    ((left)) :

    (left << ((int)right));
}

static uint32_t g_69 = 0x797CFCBFL;
static uint8_t g_22 = 0x4CL;
static int32_t g_465 = 0x5F3E33FAL;

int main() {
    // If statement that includes removal function in condition
    if (safe_lshift_func_int16_t_s_s(6, 3) > 5)
    {
        int32_t l_67 = 0L;
        if (true)
        {
            int i, j;
        }
    }
    else
    {
        int8_t l_2469 = (-1L);
        int32_t l_2487 = (-9L);
        bool l_33 = (l_2469 <= 0xA6511E7AL);
        if (l_33)
            l_2469 = (-9L);
    }

    // If statement that includes removal function in body
    if (true)
    {
        ++g_69;
        int8_t l_2469;
        int16_t l_67_copy;
        l_2469 = (-1L);  // Expression statement that is not removed
        // Expression statement that includes removal function
        int16_t l_67 = safe_lshift_func_int16_t_s_s(6, 3);  // Variable declaration that uses removal statement
        printf("%d %d", l_67, l_2469);  // Call expression that uses removed variable
        l_67_copy = l_67;  // Expression statement that uses removed variable
    }

    // For statement that includes removal function in condition
    int16_t value = 1;
    int shift_amount = 1;
    for (; safe_lshift_func_int16_t_s_s(value, shift_amount) < 1000; shift_amount++)
    {
            value = safe_lshift_func_int16_t_s_s(value, shift_amount);
            printf("Value: %d, Shift Amount: %d\n", value, shift_amount);
    }

    //  If statement contained in for statement
    for (; safe_lshift_func_int16_t_s_s(value, shift_amount) < 1000; shift_amount++)
    {
            if (true)
            {
                int16_t l_67 = safe_lshift_func_int16_t_s_s(6, 3);
            }
    }

    // For statement that includes removal function in body
    int i;
    int16_t l_68;
    for (i = 0; i < 5; i++)
    {
        l_68 = safe_lshift_func_int16_t_s_s(6, i);
    }

    if (g_22)
    {
        l_68 = safe_lshift_func_int16_t_s_s(6, i);
    }
    for (g_465 = 0; (g_465 >= 7); ++g_465)
    {
        l_68 = safe_lshift_func_int16_t_s_s(6, i);
    }
}

