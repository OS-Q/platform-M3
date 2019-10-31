// #include "stm32f1xx_ll_bus.h"
// #include "stm32f1xx_ll_rcc.h"
// #include "stm32f1xx_ll_system.h"
// #include "stm32f1xx_ll_utils.h"
// #include "stm32f1xx_ll_gpio.h"
#include "main.h"


// #define LED_PIN                 LL_GPIO_PIN_13
// #define LED_GPIO_PORT           GPIOC
#define LED_GPIO_CLK_ENABLE()   LL_APB2_GRP1_EnableClock(LL_APB2_GRP1_PERIPH_GPIOC)

void Configure_GPIO(void)
{
  LED_GPIO_CLK_ENABLE();
  LL_GPIO_SetPinMode(LED_GPIO_Port, LED_Pin, LL_GPIO_MODE_OUTPUT);
}

void SystemClock_Config(void)
{
  /* Enable HSE oscillator */
  LL_RCC_HSE_EnableBypass();
  LL_RCC_HSE_Enable();
  while(LL_RCC_HSE_IsReady() != 1)
  {
  };

  /* Set FLASH latency */
  LL_FLASH_SetLatency(LL_FLASH_LATENCY_2);
  //LL_FLASH_SetLatency(LL_FLASH_LATENCY_3);

  /* Main PLL configuration and activation */
  LL_RCC_PLL_ConfigDomain_SYS(LL_RCC_PLLSOURCE_HSE_DIV_1, LL_RCC_PLL_MUL_9);
  LL_RCC_PLL_Enable();
  // LL_RCC_PLL_ConfigDomain_SYS(LL_RCC_PLLSOURCE_HSE, LL_RCC_PLLM_DIV_8, 400, LL_RCC_PLLP_DIV_4);
  // LL_RCC_PLL_Enable();
  while(LL_RCC_PLL_IsReady() != 1)
  {
  };
  LL_RCC_SetAHBPrescaler(LL_RCC_SYSCLK_DIV_1);
  LL_RCC_SetAPB1Prescaler(LL_RCC_APB1_DIV_2);
  LL_RCC_SetAPB2Prescaler(LL_RCC_APB2_DIV_1);
  LL_RCC_SetSysClkSource(LL_RCC_SYS_CLKSOURCE_PLL);

   /* Wait till System clock is ready */
  while(LL_RCC_GetSysClkSource() != LL_RCC_SYS_CLKSOURCE_STATUS_PLL)
  {
  
  }

  // LL_SYSTICK_SetClkSource(LL_SYSTICK_CLKSOURCE_HCLK);
  LL_SetSystemCoreClock(72000000);
  LL_Init1msTick(72000000);
  /* Sysclk activation on the main PLL */
  // LL_RCC_SetAHBPrescaler(LL_RCC_SYSCLK_DIV_1);
  // LL_RCC_SetSysClkSource(LL_RCC_SYS_CLKSOURCE_PLL);
  // while(LL_RCC_GetSysClkSource() != LL_RCC_SYS_CLKSOURCE_STATUS_PLL)
  // {
  // };

  /* Set APB1 & APB2 prescaler */
  // LL_RCC_SetAPB1Prescaler(LL_RCC_APB1_DIV_2);
  // LL_RCC_SetAPB2Prescaler(LL_RCC_APB2_DIV_1);

  /* Update CMSIS variable (which can be updated also through SystemCoreClockUpdate function) */
// SystemCoreClock = SYS_CLOCK;
  
  // LL_Init1msTick(SystemCoreClock);
}



int main(void)
{
  SystemClock_Config();
  
  Configure_GPIO();
  while (1)
  {
    LL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
    LL_mDelay(1000);
  }
}

void NMI_Handler(void)
{
}

void HardFault_Handler(void)
{
  while (1) {}
}


void MemManage_Handler(void)
{
  while (1) {}
}

void BusFault_Handler(void)
{
  while (1) {}
}

void UsageFault_Handler(void)
{
  while (1) {}
}

void SVC_Handler(void)
{
}


void DebugMon_Handler(void)
{
}

void PendSV_Handler(void)
{
}
