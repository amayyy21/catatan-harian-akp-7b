elif menu == "📂 Riwayat Transaksi":
    st.title("📂 Riwayat Transaksi")

    df = pd.DataFrame(st.session_state.transactions)

    if df.empty:
        st.info("Belum ada transaksi.")
    else:
        df = filter_by_user(df, st.session_state.user)
        df["tanggal"] = pd.to_datetime(df["tanggal"])

        # =========================
        # FILTER
        # =========================
        st.subheader("🔍 Filter Transaksi")

        col1, col2, col3 = st.columns(3)

        with col1:
            f_kategori = st.multiselect(
                "Kategori",
                options=df["kategori"].unique().tolist(),
                default=df["kategori"].unique().tolist()
            )

        with col2:
            f_jenis = st.multiselect(
                "Jenis",
                options=df["jenis"].unique().tolist(),
                default=df["jenis"].unique().tolist()
            )

        with col3:
            tgl_awal, tgl_akhir = st.date_input(
                "Rentang Tanggal",
                value=[df["tanggal"].min().date(), df["tanggal"].max().date()]
            )

        dff = df[
            (df["kategori"].isin(f_kategori)) &
            (df["jenis"].isin(f_jenis)) &
            (df["tanggal"].dt.date >= tgl_awal) &
            (df["tanggal"].dt.date <= tgl_akhir)
        ].sort_values("tanggal", ascending=False)

        st.markdown("### 📄 Data Transaksi")
        st.dataframe(dff, use_container_width=True)

        # =========================
        # HAPUS TRANSAKSI
        # =========================
        st.markdown("### ❌ Hapus Transaksi (Jika Salah Input)")

        idx_to_delete = st.multiselect(
            "Pilih transaksi yang ingin dihapus",
            options=dff.index,
            format_func=lambda x: f"{dff.loc[x,'tanggal'].strftime('%d-%m-%Y')} | "
                                   f"{dff.loc[x,'jenis']} | "
                                   f"Rp {dff.loc[x,'jumlah']:,.0f} | "
                                   f"{dff.loc[x,'kategori']}"
        )

        if idx_to_delete:
            if st.button("🗑️ Hapus Transaksi Terpilih"):
                st.session_state.transactions = [
                    t for i, t in enumerate(st.session_state.transactions)
                    if i not in idx_to_delete
                ]
                st.success("Transaksi berhasil dihapus ✅")
                st.experimental_rerun()
