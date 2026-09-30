import random
import streamlit as st

LINHAS_VITORIA = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

SIMBOLOS = {"X": "❌", "O": "⭕", "": " "}


def verificar_vencedor(tab):
    """Retorna (vencedor, linha_vencedora).
    vencedor pode ser 'X', 'O', 'Empate' ou 'None'(jogo em andamento)."""
    for a, b, c in LINHAS_VITORIA:
        if tab[a] and tab[a] == tab[b] == tab[c]:
            return tab[a], (a, b, c)
    if all(tab):
        return "Empate", ()
    return None, ()


def minimax(tab, jogador):
    """Algoritmo minimax: o computador é 'O' (maximiza) e o humano é 'X' (minimiza)."""
    vencedor, _ = verificar_vencedor(tab)
    if vencedor == "O":
        return 1
    elif vencedor == "X":
        return -1
    elif vencedor == "Empate":
        return 0

    pontuacoes = []
    for i in range(9):
        if tab[i] == "":
            tab[i] = jogador
            pontuacoes.append(minimax(tab, "X" if jogador == "O" else "O"))
            tab[i] = ""
    return max(pontuacoes) if jogador == "O" else min(pontuacoes)


def melhor_jogada(tab):
    """Escolhe a jogada com maior pontuação (computador imbatível)."""
    melhor_pontuacao, melhores = -2, []
    for i in range(9):
        if tab[i] == "":
            tab[i] = "O"
            pontuacao = minimax(tab, "X")
            tab[i] = ""
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao, melhores = pontuacao, [i]
            elif pontuacao == melhor_pontuacao:
                melhores.append(i)
    return random.choice(melhores)


def jogada_aleatoria(tab):
    return random.choice([i for i in range(9) if tab[i] == ""])


# Estado (st.session_state guarda os dados entre as interações)


def novo_jogo():
    st.session_state.tabuleiro = [""] * 9
    st.session_state.turno = "X"
    st.session_state.vencedor = None
    st.session_state.linha_vitoria = ()


def zerar_placar():
    st.session_state.placar = {"X": 0, "O": 0, "Empate": 0}
    novo_jogo()


if "placar" not in st.session_state:
    zerar_placar()


def registrar_resultado():
    vencedor, linha = verificar_vencedor(st.session_state.tabuleiro)
    if vencedor:
        st.session_state.vencedor = vencedor
        st.session_state.linha_vitoria = linha
        st.session_state.placar[vencedor] += 1
        return True
    return False


def jogar(i):
    """Callback chamado quando uma casa é clicada."""
    print("clicou na casa", i, "| tabuleiro:", st.session_state.tabuleiro)
    tab = st.session_state.tabuleiro
    if tab[i] != "" or st.session_state.vencedor:
        return

    tab[i] = st.session_state.turno
    if registrar_resultado():
        return
    st.session_state.turno = "O" if st.session_state.turno == "X" else "X"

    modo = st.session_state.modo
    if modo != "2 jogadores" and st.session_state.turno == "O":
        if modo == "Contra o computador (fácil)":
            j = jogada_aleatoria(tab)
        else:
            j = melhor_jogada(tab)
        tab[j] = "O"
        if registrar_resultado():
            return
        st.session_state.turno = "X"


# INTERFACE

st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")
st.title("🎮 ❌Jogo da Velha⭕")

st.selectbox(
    "Modo de Jogo",
    ["2 jogadores", "Contra o computador (fácil)", "Contra o computador (imbatível)"],
    key="modo",
    on_change=zerar_placar,
)


# PLACAR
p = st.session_state.placar
c1, c2, c3 = st.columns(3)
c1.metric("❌ Jogador X", p["X"])
c2.metric("🤝 Empates", p["Empate"])
c3.metric(
    "⭕ Jogador O" if st.session_state.modo == "2 jogadores" else "⭕ Computador",
    p["O"],
)


# STATUS
vencedor = st.session_state.vencedor
if vencedor == "Empate":
    st.info("Deu Empate! 🤝")
elif vencedor:
    st.success(f"{SIMBOLOS[vencedor]} venceu! 🎉🎉🎉")
else:
    st.write(f"Vez de: **{SIMBOLOS[st.session_state.turno]}**")


# TABULEIRO
for linha in range(3):
    colunas = st.columns(3)
    for coluna in range(3):
        i = linha * 3 + coluna
        valor = st.session_state.tabuleiro[i]
        colunas[coluna].button(
            SIMBOLOS[valor],
            key=f"casa_{i}",
            on_click=jogar,
            args=(i,),
            use_container_width=True,
            disabled=bool(valor) or bool(vencedor),
            type="primary" if i in st.session_state.linha_vitoria else "secondary",
        )

st.divider()
b1,b2 = st.columns(2)
b1.button("🔄 Nova partida", on_click=novo_jogo, use_container_width=True)
b2.button("🗑️ Zerar placar", on_click=zerar_placar, use_container_width=True)
