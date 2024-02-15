<template>
  <div class="background-page wt-border">
    <div class="q-pl-lg q-pb-xl q-pt-lg ">
      <h5 class="q-mb-lg title-style">Quem somos</h5>

      <div class="q-mb-xl">
        <h4 class="q-mb-xs row items-center title-style">
          <q-icon
            size="sm"
            color="warning"
            name="work_outline"
            class="q-mr-sm"
          />
          A empresa
        </h4>
        <p>
          A WATCH TIME é assistência técnica autorizada das marcas Audemars
          Piguet, Parmigiani Fleurier, Ulysse Nardin, Chopard, Hublot, Graham,
          Zenith, Bvlgari, Omega, Breitling, TAG Heuer, Rado, Longines, Tissot,
          Mido e Swatch.
        </p>
        <q-separator />
      </div>
      <div class="q-mb-xl">
        <h4 class="q-mb-xs row items-center title-style">
          <q-icon size="sm" color="warning" name="history" class="q-mr-sm" />
          História
        </h4>
        <p>
          Estabelecida em 2001, nossa equipe é composta por profissionais com
          mais de 25 anos de experiência no ramo relojoeiro.
        </p>
        <q-separator />
      </div>

      <div class="q-mb-xl">
        <h4 class="q-mb-xs row items-center title-style">
          <q-icon
            size="sm"
            color="warning"
            name="settings"
            class="q-mr-sm"
          />Infraestrutura
        </h4>
        <p>
          Atendimento Nacional com escritórios e oficinas em SP, RJ e Curitiba.
        </p>
        <q-separator />
      </div>

      <q-timeline color="warning q-ml-xs">
        <h4 class="q-mb-lg title-style">
          <q-icon
            size="sm"
            color="warning"
            name="check_circle_outline"
            class="q-mr-sm"
          />Missão / Visão / Valores
        </h4>

        <q-timeline-entry subtitle="Missão" class="q-ml-lg">
          <div>
            Nossa missão é assistir aos nossos clientes, parceiros e
            fornecedores com o melhor pós-venda e assistência técnica, trazendo
            ao mercado brasileiro um serviço de alta qualidade e tecnologia, de
            acordo com as diretrizes de qualidade das manufaturas suíças de
            maior prestígio.
          </div>
        </q-timeline-entry>

        <q-timeline-entry subtitle="Visão" class="q-ml-lg">
          <div>
            Ser reconhecida como a melhor Assistência Técnica de Relógios do
            Brasil.
          </div>
        </q-timeline-entry>

        <q-timeline-entry subtitle="Valores" class="q-ml-lg">
          <div>
            Transparência, responsabilidade, comprometimento e ética são nossos
            valores fundamentais e são refletidos em todos os nossos
            funcionários.
          </div>
        </q-timeline-entry>
      </q-timeline>
      <q-separator />

      <div>
        <h4 class="q-mb-xs q-mt-lg row items-center title-style">
          <q-icon
            size="sm"
            color="warning"
            name="timeline"
            class="q-mr-sm"
          />Qualidade
        </h4>
        <p>
          A WATCH TIME se compromete com o atendimento aos requisitos dos
          fabricantes e com a melhoria contínua da eficácia do sistema de gestão
          da qualidade. Qualidade em 1° lugar.
        </p>
      </div>
    </div>
  </div>
</template>
<script>
export default {};
</script>

<style lang="scss" scoped>
img {
  filter: grayscale(100%) blur(7px);
}

h4 {
  font-size: 16px;
}

.background-page {
  background: white;
}
</style>
