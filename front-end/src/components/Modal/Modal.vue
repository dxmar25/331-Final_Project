<script>
export default {
    props: {
        show: Boolean,
        close: Function,
        size: {
            type: String,
            default: 'medium'
        },
    },
    computed: {
        classes() {
            return [
                `modal-${this.size}`,
                this.class
            ];
        }
    }
}
</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask overflow-scroll">
            <div class="modal-wrapper">
                <div class="modal-container relative" :class="classes">
                    <div class="modal-header">
                        <slot name="header">default header</slot>
                    </div>

                    <div class="modal-body">
                        <slot name="body">default body</slot>
                    </div>

                    <div class=" modal-footer fixed bottom-[5.5vh] bg-black">
                        <slot name="footer">

                            <button class="modal-default-button" @click="$emit('close')">OK</button>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style>
.modal-small {
    width: 320px
}

.modal-medium {
    width: 480px;
}

.modal-large {
    width: 680px;
}

.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}

.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}

.modal-container {
    height: 90vh;
    overflow-y: scroll;
    margin: auto;
    padding: 5px 15px;
    background-color: #fff;
    color: black;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
}

.modal-header h3 {
    margin-top: 0;
    color: #42b983;
}

.modal-body {
    margin: 15px 0;
}

.modal-default-button {
    float: right;
    background-color: maroon;
    color: white;
    padding: 10px 20px;
    border-radius: 3px;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
    opacity: 0;
}

.modal-leave-to {
    opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
}
</style>
